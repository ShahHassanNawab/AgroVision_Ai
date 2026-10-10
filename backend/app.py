"""
backend/app.py
==============
Integrated FastAPI server for the NovaMind Crop Disease Detection Platform.
Coordinates on-device deep learning inference (MobileNetV2), genuine Grad-CAM explainability,
Google Gemini Vision agronomic analysis, and live Gemini Agronomy Chatbot.
"""

import os
import io
import time
import json
import uuid
import logging
from contextlib import asynccontextmanager
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("VerdixApp")

# ─────────────────────────────────────────────────────────────────────────────
# Paths & Configuration
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
HISTORY_FILE = DATA_DIR / "history.json"
FRONTEND_DIR = BASE_DIR / "frontend"

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB limit


# ─────────────────────────────────────────────────────────────────────────────
# Scan history persistence
# ─────────────────────────────────────────────────────────────────────────────

def load_history() -> List[Dict[str, Any]]:
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read history: {e}")
            return []
    return []


def save_history(history: List[Dict[str, Any]]) -> None:
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to write history: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Lifespan: Load model and services once at startup
# ─────────────────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Initializing NovaMind Crop Disease Detection Backend Services …")

    from backend.model_runner import ModelRunner
    from backend.gemini_analyzer import GeminiAnalyzer

    weights_path = os.getenv("MODEL_WEIGHTS_PATH") or None
    application.state.model_runner = ModelRunner(weights_path=weights_path)
    application.state.gemini_analyzer = GeminiAnalyzer()
    application.state.scan_history = load_history()

    runner = application.state.model_runner
    gemini = application.state.gemini_analyzer

    logger.info(
        f"Deep Learning Model: {'✓ Active (' + runner.framework + ')' if runner.model_loaded else '— Standby (no weights/library)'}"
    )
    logger.info(
        f"Gemini Vision Engine: {'✓ Configured (Live API active)' if gemini.is_configured() else '— Standby (no GEMINI_API_KEY in .env)'}"
    )
    logger.info("Backend service initialization complete.")

    yield

    logger.info("Shutting down NovaMind Backend …")
    application.state.model_runner = None
    application.state.gemini_analyzer = None


def get_model_runner():
    runner = getattr(app.state, "model_runner", None)
    if runner is None:
        from backend.model_runner import ModelRunner
        weights_path = os.getenv("MODEL_WEIGHTS_PATH") or None
        runner = ModelRunner(weights_path=weights_path)
        app.state.model_runner = runner
    return runner


def get_gemini_analyzer():
    gemini = getattr(app.state, "gemini_analyzer", None)
    if gemini is None:
        from backend.gemini_analyzer import GeminiAnalyzer
        gemini = GeminiAnalyzer()
        app.state.gemini_analyzer = gemini
    return gemini


def get_scan_history() -> List[Dict[str, Any]]:
    history = getattr(app.state, "scan_history", None)
    if history is None:
        history = load_history()
        app.state.scan_history = history
    return history


# ─────────────────────────────────────────────────────────────────────────────
# FastAPI App Definition
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="NovaMind Plant Disease Detection & Agronomy API",
    description=(
        "Production-grade API combining trained MobileNetV2 on-device deep learning "
        "(38 PlantVillage classes), genuine Grad-CAM explainability, and Google Gemini Vision."
    ),
    version="2.1.0",
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
# Helper: Secure Image Ingestion
# ─────────────────────────────────────────────────────────────────────────────

async def _read_and_validate_image(upload: UploadFile) -> Tuple[bytes, Image.Image]:
    """
    Validates MIME type, file size, and decodes the image securely.
    Guarantees no arbitrary filesystem paths are used.
    """
    if not upload.content_type or not upload.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"File '{upload.filename}' is not a supported image format. "
                "Please upload a valid JPEG, PNG, or WEBP image."
            ),
        )

    try:
        content = await upload.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read image stream: {e}",
        )

    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded image file is empty.",
        )

    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image size exceeds the maximum allowed limit of {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.",
        )

    try:
        pil_image = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Corrupt or unreadable image file: {e}",
        )

    return content, pil_image


# ─────────────────────────────────────────────────────────────────────────────
# Pydantic Schemas
# ─────────────────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None
    diagnosis_context: Optional[Dict[str, Any]] = None


# ─────────────────────────────────────────────────────────────────────────────
# System & Health Endpoints (PHASE 3-A)
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/health", tags=["System"])
async def get_health_status():
    """
    Health check endpoint reporting backend operational status,
    model loader state, and Gemini configuration.
    """
    runner = get_model_runner()
    gemini = get_gemini_analyzer()

    model_ready = bool(runner and runner.model_loaded)
    gemini_ready = bool(gemini and gemini.is_configured())

    return {
        "status": "healthy",
        "service": "NovaMind Crop Disease Detection Platform",
        "model_loaded": model_ready,
        "framework": runner.framework if runner else None,
        "weights_path": runner.weights_path if runner else None,
        "total_classes": len(runner.class_names) if runner else 0,
        "gemini_active": gemini_ready,
        "timestamp": time.time(),
    }


@app.get("/api/status", tags=["System"])
async def get_system_status():
    """Legacy/extended system status check."""
    runner = get_model_runner()
    gemini = get_gemini_analyzer()
    history = get_scan_history()
    return {
        "status": "online",
        "service": "NovaMind Plant Disease Detection API",
        "gemini_configured": gemini.is_configured(),
        "model_loaded": runner.model_loaded,
        "framework": runner.framework,
        "weights_path": runner.weights_path,
        "total_classes": len(runner.class_names),
        "total_scans": len(history),
    }


@app.get("/classes", tags=["Reference"])
def get_classes():
    """List all 38 PlantVillage disease classes supported by the trained model."""
    runner = get_model_runner()
    names = runner.class_names if runner else []
    return {
        "total_classes": len(names),
        "classes": names,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Disease Prediction Endpoint (PHASE 3-B)
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/predict", tags=["Prediction"])
async def predict_endpoint(
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
):
    """
    Pure deep learning model prediction endpoint.
    Accepts multipart/form-data with field 'file' or 'image'.
    Returns structured model predictions, top candidates, lesion severity,
    and genuine Grad-CAM explainability heatmap.
    """
    upload = file or image
    if upload is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image uploaded. Please provide an image using form field 'file' or 'image'.",
        )

    _, pil_image = await _read_and_validate_image(upload)

    runner = get_model_runner()
    result = runner.predict(pil_image)

    if not result.get("success"):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE if not runner.model_loaded else status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "filename": upload.filename,
                "message": result.get("message") or result.get("error") or "Inference unavailable.",
                "model_loaded": runner.model_loaded,
            },
        )

    return {
        "success": True,
        "filename": upload.filename,
        "predicted_class": result["disease_name"],
        "raw_class": result["predicted_class"],
        "crop": result["crop"],
        "condition": result["condition"],
        "is_healthy": result["is_healthy"],
        "scientific_name": result["scientific_name"],
        "confidence": result["confidence"],
        "confidence_percentage": result["confidence_percentage"],
        "class_probabilities": result.get("class_probabilities", {}),
        "top_predictions": result.get("top_predictions", []),
        "severity": result["severity"],
        "severity_percentage": result["severity_percentage"],
        "severity_method": result["severity_method"],
        "heatmap_available": result["heatmap_available"],
        "heatmap_url": result["heatmap"] if result["heatmap_available"] else None,
        "score": result["score"],
        "treatment": result.get("treatment", []),
        "prevention": result.get("prevention", []),
        "model_mode": result.get("model_mode", "real_model"),
    }


# Also keep /predict route for backwards compatibility
@app.post("/predict", tags=["Prediction"])
async def predict_alias(
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
):
    return await predict_endpoint(file=file, image=image)


# ─────────────────────────────────────────────────────────────────────────────
# Comprehensive Leaf Diagnosis Endpoint (Frontend Primary)
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/diagnose", tags=["Diagnosis"])
async def diagnose_leaf(image: UploadFile = File(...)):
    """
    Main diagnostic endpoint coordinating on-device model inference and
    Gemini agronomy synthesis.
    """
    _, pil_image = await _read_and_validate_image(image)

    runner = get_model_runner()
    gemini = get_gemini_analyzer()

    # 1. Run on-device deep learning model
    local_result = runner.predict(pil_image)

    # 2. Run Gemini Vision reasoning with model context
    gemini_result = gemini.analyze(pil_image, local_model_context=local_result)

    # 3. Determine heatmap: prefer genuine Grad-CAM from model
    heatmap = local_result.get("heatmap") or gemini_result.get("heatmap", "")

    # 4. Integrate results
    diagnosis_id = str(uuid.uuid4())
    disease_name = (
        local_result.get("disease_name")
        or gemini_result.get("name")
        or "Plant Condition"
    )
    confidence = float(
        local_result.get("confidence")
        if local_result.get("confidence") is not None
        else (gemini_result.get("confidence") or 0.88)
    )
    health_score = int(
        local_result.get("score")
        if local_result.get("score") is not None
        else gemini_result.get("score", 50)
    )
    severity = str(local_result.get("severity") or gemini_result.get("severity", "Moderate"))

    # Detect low confidence or potential out-of-distribution leaf image
    is_low_confidence = bool(confidence < 0.28 and not local_result.get("is_healthy", False))

    response_data: Dict[str, Any] = {
        "id": diagnosis_id,
        "name": disease_name,
        "crop": local_result.get("crop") or "Crop",
        "condition": local_result.get("condition") or "Condition",
        "is_healthy": local_result.get("is_healthy", False),
        "scientific_name": local_result.get("scientific_name", "N/A"),
        "confidence": confidence,
        "confidence_percentage": f"{round(confidence * 100, 1)}%",
        "score": health_score,
        "severity": severity,
        "severity_percentage": local_result.get("severity_percentage"),
        "severity_method": local_result.get("severity_method"),
        "summary": gemini_result.get("summary") or local_result.get("summary", ""),
        "treatment": list(gemini_result.get("treatment") or local_result.get("treatment", [])),
        "prevention": list(gemini_result.get("prevention") or local_result.get("prevention", [])),
        "symptoms": list(local_result.get("symptoms", [])),
        "precautions": local_result.get("precautions", ""),
        "heatmap": heatmap,
        "heatmap_available": bool(heatmap),
        "local_prediction": local_result.get("disease_name"),
        "local_confidence": local_result.get("confidence"),
        "top_predictions": local_result.get("top_predictions", []),
        "demo": bool(gemini_result.get("demo", False)),
        "model_loaded": runner.model_loaded,
        "framework": runner.framework,
        "is_low_confidence": is_low_confidence,
        "unsupported_crop": is_low_confidence,
        "ts": time.time(),
    }

    # Persist lightweight scan record
    scan_history = get_scan_history()
    scan_history.insert(0, {
        "id": diagnosis_id,
        "name": response_data["name"],
        "confidence": response_data["confidence"],
        "score": response_data["score"],
        "severity": response_data["severity"],
        "ts": response_data["ts"],
    })
    save_history(scan_history)

    return response_data


# ─────────────────────────────────────────────────────────────────────────────
# Conversational Gemini Agronomy Chatbot Endpoint (PHASE 7)
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/chat", tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    """
    Dedicated endpoint for the Gemini Agronomy Chatbot.
    Maintains diagnosis context and multi-turn history.
    """
    gemini = get_gemini_analyzer()
    if not gemini or not gemini.is_configured():
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "success": False,
                "response": "Gemini API key is not configured on the server. Please check your .env configuration.",
                "model_used": None,
            },
        )

    user_msg = (request.message or "").strip()
    if not user_msg:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty.",
        )

    # Format history as dict list
    history_dicts = []
    if request.history:
        for m in request.history:
            history_dicts.append({"role": m.role, "content": m.content})

    result = gemini.chat(
        user_message=user_msg,
        history=history_dicts,
        diagnosis_context=request.diagnosis_context,
    )

    if not result.get("success"):
        status_code = (
            status.HTTP_503_SERVICE_UNAVAILABLE
            if result.get("service_unavailable")
            else status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return JSONResponse(
            status_code=status_code,
            content=result,
        )

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Analytics & History Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/history", tags=["Analytics"])
async def get_history():
    """Returns the 50 most recent diagnosis scan records."""
    return get_scan_history()[:50]


@app.get("/api/field", tags=["Analytics"])
async def get_field_stats():
    """Aggregated field health metrics over the past 7 days."""
    history = get_scan_history()
    total = len(history)
    now = time.time()
    week_ago = now - (7 * 86400)

    recent = [s for s in history if s.get("ts", 0) >= week_ago]
    alerts = sum(1 for s in recent if str(s.get("severity", "")).lower() == "severe")

    if recent:
        avg_health = round(sum(s.get("score", 50) for s in recent) / len(recent))
    elif total > 0:
        avg_health = round(sum(s.get("score", 50) for s in history) / total)
    else:
        avg_health = None

    return {
        "health": avg_health,
        "alerts": alerts,
        "scans_week": len(recent),
        "total": total,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Static Frontend Serving
# ─────────────────────────────────────────────────────────────────────────────

if FRONTEND_DIR.exists():
    @app.get("/", include_in_schema=False)
    async def serve_index():
        for filename in ("index.html", "novamind.html"):
            index_file = FRONTEND_DIR / filename
            if index_file.exists():
                return FileResponse(str(index_file))
        return JSONResponse(content={"message": "NovaMind API running. Frontend index.html not found."})

    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    uvicorn.run("backend.app:app", host=host, port=port, reload=debug)
