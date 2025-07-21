import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
import os

# 3. Define the class names (in alphabetical order) 
#    Your 'get_data' function found these from the sub-directory names.
CLASS_NAMES = ['mustang', 'not_mustang'] # Example: Change if your folder names are different

# Global variable to store the loaded model
_model = None

def load_model(model_path):
    """Load the model from the given path."""
    global _model
    if _model is None:
        print(f"Loading model from: {model_path}")
        _model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully.")
    return _model

# --- Prediction Function ---
def predict_image(model_path, img_path):
    """Loads and preprocesses an image, then returns the model's prediction and confidence."""
    try:
        # Load the model if not already loaded
        model = load_model(model_path)
        
        # Load the image, resizing it to the target size your model expects
        img = image.load_img(img_path, target_size=(260, 260))

        # Convert the image to a NumPy array
        img_array = image.img_to_array(img)
        
        # Expand the dimensions to create a "batch" of 1
        img_batch = np.expand_dims(img_array, axis=0)
        
        # Preprocess the image for the EfficientNetB0 model
        img_preprocessed = preprocess_input(img_batch)
        
        # Make the prediction
        prediction = model.predict(img_preprocessed)
        prediction_value = prediction[0][0]
        
        # Interpret the prediction
        # The model outputs a single value between 0 and 1 because of the sigmoid activation
        # We use 0.5 as a threshold to decide the class
        if prediction_value < 0.5:
            predicted_class = CLASS_NAMES[0]  # 'mustang'
            confidence = (1 - prediction_value) * 100  # Convert to percentage
        else:
            predicted_class = CLASS_NAMES[1]  # 'not_mustang'
            confidence = prediction_value * 100  # Convert to percentage
            
        return predicted_class, round(confidence, 2)
        
    except Exception as e:
        print(f"Error in predict_image: {str(e)}")
        raise e

# --- Main execution ---
if __name__ == '__main__':
    # Configuration for standalone testing
    MODEL_PATH = r"./models/mustang_classifier_model_v0_5.h5"
    IMG_PATH = 'path/to/your/test_image.jpg'  # Change this to your image path

    try:
        # Make prediction
        predicted_class, confidence = predict_image(MODEL_PATH, IMG_PATH)

        print("\n--- Prediction ---")
        print(f"Image: {IMG_PATH}")
        print(f"The model predicts this is a: {predicted_class}")
        print(f"Confidence: {confidence}%")
        print("------------------")
    except Exception as e:
        print(f"Error: {str(e)}")