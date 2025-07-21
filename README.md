# Mustang Classifier Web Interface

https://mus-classifier-main-production.up.railway.app

A Flask-based web application for testing the legacy Mustang Classifier deep learning model. This project provides a user-friendly interface to classify images of Ford Mustangs, specifically distinguishing between S650 and S550 generation models.

## 🚗 About

This is a testing and demonstration platform for a pre-production machine learning model designed to identify Ford Mustang vehicles. While the model was originally trained for broader car classification, it has been specialized to accurately identify S650 and S550 generation Ford Mustangs.

## 🏗️ Project Structure

```
Mustang-Classifier-Legacy-Web/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── models/                      # Trained model files
│   ├── mustang_classifier_model_v0_4.h5
│   ├── mustang_classifier_model_v0_5.h5  # Current model
│   ├── mustang_classifier_model.h5
│   └── mustang_classifier_model.keras
└── webfront/                    # Web application
    ├── app.py                   # Main Flask application
    ├── app_fixed.py             # Alternative app version
    ├── test_model.py            # Model prediction logic
    ├── start_app.bat            # Windows startup script
    └── templates/
        └── index.html           # Web interface template
```

## ✨ Features

- **Web-based Interface**: Upload images through a modern, responsive web interface
- **Real-time Classification**: Instant predictions with confidence scores
- **Multiple Model Versions**: Support for different model iterations
- **File Format Support**: Accepts PNG, JPG, and JPEG images
- **Visual Feedback**: Displays uploaded images alongside predictions
- **Error Handling**: Comprehensive error messages and validation

## 🧠 Model Details

- **Architecture**: Based on EfficientNetB0 with transfer learning
- **Input Size**: 260x260 pixels
- **Output**: Binary classification (Mustang vs Not Mustang)
- **Framework**: TensorFlow/Keras
- **Preprocessing**: EfficientNet-specific preprocessing pipeline

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sayanwala117/Mustang-Classifier-Legacy-Web.git
   cd Mustang-Classifier-Legacy-Web
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   
   **Option A: Using Python directly**
   ```bash
   cd webfront
   python app.py
   ```
   
   **Option B: Using the batch script (Windows)**
   ```bash
   cd webfront
   start_app.bat
   ```

4. **Access the application**
   Open your web browser and navigate to: `http://127.0.0.1:5000`

## 📖 Usage

1. **Upload an Image**: Click "Choose File" and select an image of a car (PNG, JPG, or JPEG)
2. **Get Prediction**: Click "Classify Image" to run the model
3. **View Results**: See the classification result and confidence percentage
4. **Try Another**: Upload another image to test different vehicles

## 🔧 Configuration

### Model Selection
The application uses `mustang_classifier_model_v0_5.h5` by default. To use a different model:

1. Edit `MODEL_PATH` in `webfront/app.py`:
   ```python
   MODEL_PATH = "../models/your_model_name.h5"
   ```

### Upload Settings
- **Max file size**: 16MB (configurable in `app.py`)
- **Allowed formats**: PNG, JPG, JPEG
- **Upload folder**: `../uploads` (auto-created)

## 🎯 Model Performance

The current model (v0.5) specializes in:
- **S650 Generation Mustangs** (2024+): Latest generation Ford Mustang
- **S550 Generation Mustangs** (2015-2023): Previous generation Ford Mustang
- **General Mustang Detection**: Distinguishing Mustangs from other vehicles

## 🛠️ Development

### File Structure
- `app.py`: Main Flask application with routing and file handling
- `test_model.py`: Model loading and prediction logic
- `index.html`: Frontend interface with modern styling
- `requirements.txt`: All necessary Python packages

### Key Components
- **Flask Web Server**: Handles HTTP requests and file uploads
- **TensorFlow Model**: Performs image classification
- **Image Preprocessing**: Resizes and normalizes input images
- **Result Processing**: Converts model output to user-friendly format

## 📊 Technical Specifications

- **Framework**: Flask (Python web framework)
- **ML Library**: TensorFlow 2.19.0, Keras 3.7.0
- **Image Processing**: PIL/Pillow via Keras preprocessing
- **Frontend**: HTML5, CSS3 with responsive design
- **File Handling**: Werkzeug secure filename utilities

## ⚠️ Limitations

- Model is optimized for Ford Mustang classification specifically
- Best performance on clear, well-lit images of vehicles
- May require retraining for other car models or generations
- Web interface is designed for single-image classification

## 🤝 Contributing

This is a testing platform for a legacy model. For improvements or bug reports:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of a pre-production research initiative. Please check with the repository owner for usage rights and licensing information.

## 🔮 Future Enhancements

- Support for batch image processing
- Model comparison interface
- Enhanced visualization of predictions
- REST API endpoints for programmatic access
- Docker containerization for easy deployment
