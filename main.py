"""
main.py — Standalone FastAPI application for Plant Disease Classification
=========================================================================
This is an independent, self-contained FastAPI server that loads the
MobileNetV2 Keras model directly (without the backend/ package).

Use this file if you want a lightweight single-file server.
Use run.py / backend/app.py if you want the full NovaMind stack
(Gemini Vision + heatmap + history + frontend serving).

Run:
    uvicorn main:app --host 127.0.0.1 --port 8000 --reload

Or:
    python main.py
"""

import io
import json
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from typing import List, Dict, Any, Optional

import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
logger = logging.getLogger("PlantDiseaseAPI")

# ─────────────────────────────────────────────────────────────────────────────
# Paths — check root first, then weights/ directory
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

_MODEL_CANDIDATES = [
    BASE_DIR / "plantvillage_mobilenet_93.h5",
    BASE_DIR / "weights" / "plantvillage_mobilenet_93.h5",
]
MODEL_PATH = next((p for p in _MODEL_CANDIDATES if p.exists()), None)

_CLASS_CANDIDATES = [
    BASE_DIR / "class_names.json",
    BASE_DIR / "weights" / "class_names.json",
]
CLASSES_PATH = next((p for p in _CLASS_CANDIDATES if p.exists()), None)

TARGET_SIZE = (224, 224)
MAX_FILE_BYTES = 10 * 1024 * 1024   # 10 MB


# ─────────────────────────────────────────────────────────────────────────────
# Helper — class name formatter
# ─────────────────────────────────────────────────────────────────────────────

def format_class_name(raw: str) -> Dict[str, Any]:
    """
    'Tomato___Early_blight' →
        {raw_name, formatted_name, crop, condition, is_healthy}
    """
    if "___" in raw:
        crop_raw, cond_raw = raw.split("___", 1)
    else:
        crop_raw, cond_raw = raw, "Condition"

    crop = crop_raw.replace("_", " ").strip()
    condition = cond_raw.replace("_", " ").strip()
    is_healthy = "healthy" in raw.lower()

    formatted = f"{crop} (Healthy)" if is_healthy else f"{crop} - {condition}"

    return {
        "raw_name": raw,
        "formatted_name": formatted,
        "crop": crop,
        "condition": condition,
        "is_healthy": is_healthy,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Helper — image preprocessing
# ─────────────────────────────────────────────────────────────────────────────

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Decode → RGB → resize (224×224) → float32 → MobileNetV2 normalise [-1, 1]
    → add batch dim → shape (1, 224, 224, 3).
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Corrupted or unreadable image file: {e}",
        )

    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize(TARGET_SIZE, Image.Resampling.BILINEAR)
    arr = np.array(image, dtype=np.float32)

    # MobileNetV2 standard normalisation: [0, 255] → [-1, 1]
    arr = (arr / 127.5) - 1.0

    return np.expand_dims(arr, axis=0)   # (1, 224, 224, 3)


# ─────────────────────────────────────────────────────────────────────────────
# Lifespan — load model + class names once
# ─────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Initialising Plant Disease Classification Service …")

    # Load class names
    if CLASSES_PATH is None:
        logger.error("class_names.json not found in root or weights/ directory.")
        application.state.class_names = []
    else:
        try:
            with open(CLASSES_PATH, "r", encoding="utf-8") as f:
                application.state.class_names = json.load(f)
            logger.info(
                f"Loaded {len(application.state.class_names)} classes from "
                f"{CLASSES_PATH.name}"
            )
        except Exception as e:
            logger.error(f"Failed to read {CLASSES_PATH}: {e}")
            application.state.class_names = []

    # Load Keras model
    if MODEL_PATH is None:
        logger.warning(
            "plantvillage_mobilenet_93.h5 not found. "
            "Place the file in the project root or weights/ directory."
        )
        application.state.model = None
    else:
        try:
            import tensorflow as tf

            logger.info(f"Loading Keras model from {MODEL_PATH} …")
            application.state.model = tf.keras.models.load_model(
                str(MODEL_PATH), compile=False
            )
            logger.info("✓ MobileNetV2 model loaded successfully.")
        except ImportError:
            logger.error(
                "TensorFlow is not installed. Run: pip install tensorflow"
            )
            application.state.model = None
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            application.state.model = None

    yield

    logger.info("Shutting down …")
    application.state.model = None
    application.state.class_names = []


# ─────────────────────────────────────────────────────────────────────────────
# Application
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Plant Disease Classification API",
    description=(
        "MobileNetV2 classifier trained on 38 PlantVillage disease classes. "
        "Upload a leaf image to receive the predicted disease and confidence score."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/", tags=["System"])
def get_root():
    """Service health check and endpoint directory."""
    model_loaded = getattr(app.state, "model", None) is not None
    classes_count = len(getattr(app.state, "class_names", []))
    return {
        "status": "online",
        "service": "Plant Disease MobileNetV2 Classification API",
        "model_loaded": model_loaded,
        "total_classes": classes_count,
        "endpoints": {
            "POST /predict": "Upload a leaf image (field: 'file') → predicted class + confidence",
            "GET  /classes": "List all 38 PlantVillage disease class names",
        },
    }


@app.get("/classes", tags=["Reference"])
def get_classes():
    """Return all 38 PlantVillage class names the model can predict."""
    class_names = getattr(app.state, "class_names", [])
    if not class_names:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Class names are not loaded. Check that class_names.json exists.",
        )
    return {
        "total_classes": len(class_names),
        "classes": [
            {"index": i, "raw": name, "formatted": format_class_name(name)["formatted_name"]}
            for i, name in enumerate(class_names)
        ],
    }


@app.post("/predict", tags=["Prediction"])
async def predict_disease(file: UploadFile = File(...)):
    """
    Plant disease prediction endpoint.

    **Request:** multipart/form-data with field `file` containing an image (JPEG/PNG/WEBP).

    **Response:**
    ```json
    {
      "success": true,
      "filename": "leaf.jpg",
      "predicted_class": "Tomato___Early_blight",
      "disease_name": "Tomato - Early Blight",
      "crop": "Tomato",
      "condition": "Early blight",
      "is_healthy": false,
      "confidence": 0.9312,
      "confidence_percentage": "93.12%",
      "top_predictions": [...top 3 classes with confidence...]
    }
    ```
    """
    # 1. Verify model and class names are ready
    model = getattr(app.state, "model", None)
    class_names: List[str] = getattr(app.state, "class_names", [])

    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Model is not loaded. Ensure plantvillage_mobilenet_93.h5 is present "
                "in the project root or weights/ directory, and TensorFlow is installed."
            ),
        )
    if not class_names:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Class names are not loaded. Check class_names.json.",
        )

    # 2. Validate MIME type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"'{file.filename}' is not a valid image "
                f"(MIME: {file.content_type}). Please upload JPEG, PNG, or WEBP."
            ),
        )

    # 3. Read file
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded file: {e}",
        )

    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )
    if len(contents) > MAX_FILE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {MAX_FILE_BYTES // (1024 * 1024)} MB limit.",
        )

    # 4. Preprocess image
    input_tensor = preprocess_image(contents)

    # 5. Run inference
    try:
        predictions = model.predict(input_tensor, verbose=0)
        probabilities: np.ndarray = predictions[0]
    except Exception as e:
        logger.error(f"Inference failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model prediction failed: {e}",
        )

    # 6. Extract top prediction
    top_index = int(np.argmax(probabilities))
    confidence = float(probabilities[top_index])
    raw_name = class_names[top_index] if top_index < len(class_names) else f"Class_{top_index}"
    info = format_class_name(raw_name)

    logger.info(
        f"Prediction: {info['formatted_name']} | confidence: {confidence:.4f} | "
        f"file: {file.filename}"
    )

    # 7. Top-3 predictions for additional context
    top3_idx = np.argsort(probabilities)[::-1][:3]
    top_predictions = []
    for idx in top3_idx:
        c_raw = class_names[idx] if idx < len(class_names) else f"Class_{idx}"
        c_info = format_class_name(c_raw)
        top_predictions.append({
            "rank": len(top_predictions) + 1,
            "class": c_raw,
            "name": c_info["formatted_name"],
            "confidence": round(float(probabilities[idx]), 4),
            "percentage": f"{round(float(probabilities[idx]) * 100, 2)}%",
        })

    # 8. Return structured response
    return {
        "success": True,
        "filename": file.filename,
        "predicted_class": raw_name,
        "disease_name": info["formatted_name"],
        "crop": info["crop"],
        "condition": info["condition"],
        "is_healthy": info["is_healthy"],
        "confidence": round(confidence, 4),
        "confidence_percentage": f"{round(confidence * 100, 2)}%",
        "top_predictions": top_predictions,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Direct run
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
