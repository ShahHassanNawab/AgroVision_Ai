# Model Weights Directory

Place your trained plant disease detection model weights in this directory.

## Supported Formats & Frameworks
The system auto-detects model files placed here:
- **PyTorch**: `.pth`, `.pt` (e.g., ResNet-50, MobileNetV2, EfficientNet trained on PlantVillage)
- **ONNX**: `.onnx`
- **TensorFlow / Keras**: `.h5`, `.keras`
- **TensorFlow Lite**: `.tflite`

## How it works:
1. When you place a model file in this folder (e.g. `weights/plant_disease_model.pth`), `backend/model_runner.py` will automatically detect and load it.
2. The model will process the uploaded leaf image to classify the disease and compute confidence/Grad-CAM.
3. The result is then synthesized with **Google Gemini Vision** for full agricultural diagnosis, disease progression analysis, active treatment schedules, and preventative recommendations.
4. If no weights file is placed here yet, the system smoothly uses **Gemini 2.5 Flash / 1.5 Flash Vision** directly to detect plant diseases from the image!
