
"""
Fixed Flask app with better error handling
"""
import os
import sys
from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename

# Add the current directory to Python path to import test_model
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from test_model import predict_image
    MODEL_IMPORT_SUCCESS = True
except ImportError as e:
    print(f"Warning: Could not import predict_image: {e}")
    MODEL_IMPORT_SUCCESS = False

MODEL_PATH = "../models/mustang_classifier_model_v0_5.h5"
UPLOAD_FOLDER = "../uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print(f"✓ Upload folder created/verified: {os.path.abspath(UPLOAD_FOLDER)}")
except Exception as e:
    print(f"✗ Could not create upload folder: {e}")

# Verify model exists
if os.path.exists(MODEL_PATH):
    print(f"✓ Model file found: {os.path.abspath(MODEL_PATH)}")
else:
    print(f"✗ Model file not found: {os.path.abspath(MODEL_PATH)}")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return f"Error serving file: {e}", 404

@app.route("/", methods=["GET", "POST"])
def home():
    """Main route for file upload and prediction"""
    try:
        print(f"Request method: {request.method}")
        print(f"Request URL: {request.url}")
        
        if request.method == "GET":
            return render_template("index.html")
        
        elif request.method == "POST":
            print("Processing POST request...")
            
            # Check if file is in request
            if 'file' not in request.files:
                print("No file in request")
                error_msg = "No file part in the request."
                return render_template("index.html", error=error_msg)

            file = request.files['file']
            print(f"File received: {file.filename}")

            # Check if file was selected
            if file.filename == '':
                print("No file selected")
                error_msg = "No file selected."
                return render_template("index.html", error=error_msg)

            # Check file type
            if not allowed_file(file.filename):
                print(f"Invalid file type: {file.filename}")
                error_msg = f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}."
                return render_template("index.html", error=error_msg)

            # Save file
            try:
                filename = secure_filename(file.filename)
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(f"Saving file to: {os.path.abspath(img_path)}")
                file.save(img_path)
                print("✓ File saved successfully")
            except Exception as e:
                print(f"✗ Error saving file: {e}")
                error_msg = f"Error saving file: {str(e)}"
                return render_template("index.html", error=error_msg)

            # Make prediction
            if MODEL_IMPORT_SUCCESS and os.path.exists(MODEL_PATH):
                try:
                    print(f"Making prediction...")
                    prediction, confidence = predict_image(MODEL_PATH, img_path)
                    print(f"✓ Prediction successful: {prediction}, confidence: {confidence}%")
                    
                    # URL path for web display
                    img_url = f"/uploads/{filename}"
                    
                    # Auto-delete the file after successful prediction
                    try:
                        if os.path.exists(img_path):
                            os.remove(img_path)
                            print(f"✓ Image file deleted: {img_path}")
                    except Exception as delete_error:
                        print(f"Warning: Could not delete image file: {delete_error}")
                    
                    return render_template("index.html", 
                                         prediction=prediction, 
                                         confidence=confidence, 
                                         img_path=None)  # Don't show image since it's deleted
                    
                except Exception as e:
                    print(f"✗ Prediction error: {e}")
                    error_msg = f"Prediction failed: {str(e)}"
                    # Clean up uploaded file on error
                    try:
                        if os.path.exists(img_path):
                            os.remove(img_path)
                    except:
                        pass
                    return render_template("index.html", error=error_msg)
            else:
                # Model not available, just show prediction without image
                print("Model not available, deleting uploaded image")
                
                # Delete the uploaded file since model is not available
                try:
                    if os.path.exists(img_path):
                        os.remove(img_path)
                        print(f"✓ Image file deleted: {img_path}")
                except Exception as delete_error:
                    print(f"Warning: Could not delete image file: {delete_error}")
                
                return render_template("index.html", 
                                     prediction="Model not available", 
                                     confidence=0, 
                                     img_path=None,
                                     error="Model not loaded - image processed but not displayed")

    except Exception as e:
        print(f"✗ Unexpected error in home route: {e}")
        import traceback
        traceback.print_exc()
        return render_template("index.html", error=f"Server error: {str(e)}")

@app.errorhandler(413)
def too_large(e):
    return render_template("index.html", error="File is too large. Maximum size is 16MB."), 413

@app.errorhandler(405)
def method_not_allowed(e):
    print(f"405 Error: Method not allowed for {request.url}")
    return render_template("index.html", error="Method not allowed"), 405

if __name__ == "__main__":
    print("Starting Flask app...")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Model path: {os.path.abspath(MODEL_PATH)}")
    print(f"Model import success: {MODEL_IMPORT_SUCCESS}")
    print("Access the app at: http://0.0.0.0:5000")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        input("Press Enter to exit...")
# --- IGNORE ---
# --- IGNORE ---
