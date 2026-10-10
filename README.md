# VerdAI / Verdix - Plant Disease Detection Platform

An AI-powered agricultural diagnosis platform connecting a modern leaf diagnosis web interface with **FastAPI**, **Google Gemini Vision**, and **On-Device Deep Learning Model Weights** (PyTorch, ONNX, TensorFlow/Keras).

---

## 📁 Project Structure

```
verdix-disease-detection/
├── backend/
│   ├── app.py                # FastAPI server (endpoints for diagnosis, history, field stats)
│   ├── gemini_analyzer.py    # Google Gemini Vision integration (Gemini 2.5/1.5 Flash)
│   ├── model_runner.py       # On-device model loader & Grad-CAM visualizer
│   └── requirements.txt      # Python dependencies
├── frontend/
│   └── index.html            # VerdAI Disease Detection UI (Camera/Upload, Grad-CAM heatmap, History, Stats)
├── weights/                  # Drop your trained model files (.pth, .pt, .onnx, .h5, etc.) here
│   └── README.md             # Weights guide
├── data/
│   └── history.json          # Persistent scan history storage
├── tests/
│   └── test_backend.py       # Automated test suite
├── .env.example              # Environment variables template
├── .env                      # Active environment configuration
├── run.py                    # One-click application launcher
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start

### 1. Launch the Server
Run the project launcher from this directory:
```bash
python run.py
```
Or with Uvicorn directly:
```bash
uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Open the Web Application
Open your browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🔑 Connecting Google Gemini Vision API

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. Open [`.env`](file:///C:/Users/HP/.gemini/antigravity-ide/scratch/verdix-disease-detection/.env) and set your key:
   ```env
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   ```
3. Restart the server or let auto-reload refresh it. The engine badge in the sidebar will switch to **Gemini: Active**!

*Note: If no API key is set, the application operates in fallback/demo mode with realistic plant disease simulations so you can test all UI flows immediately.*

---

## 🧠 Connecting Model Weights

1. Place your trained model file into the [`weights/`](file:///C:/Users/HP/.gemini/antigravity-ide/scratch/verdix-disease-detection/weights) directory.
2. Supported formats:
   - **PyTorch**: `.pth`, `.pt` (e.g., ResNet, MobileNet trained on PlantVillage 38 classes)
   - **ONNX**: `.onnx`
   - **TensorFlow / Keras**: `.h5`, `.keras`, `.tflite`
3. The server auto-detects model files in `weights/` upon startup and runs on-device inference combined with Gemini's agronomy reasoning!

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/diagnose` | Accepts `image` (multipart/form-data), returns disease name, confidence, score, treatment, prevention & Grad-CAM heatmap |
| `GET` | `/api/history` | Returns previous scan records with timestamps and severity |
| `GET` | `/api/field` | Returns aggregate statistics (field health score, active alerts, weekly scans) |
| `GET` | `/api/status` | Returns system status (Gemini API state, loaded model framework & weights) |
| `GET` | `/` | Serves the VerdAI web user interface |
