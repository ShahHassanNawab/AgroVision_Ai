"""
tests/test_backend.py
=====================
Comprehensive integration test suite for the NovaMind Crop Disease Detection Platform.
Tests health checks, model predictions, lesion severity estimation,
agronomy chatbot, input validation, and history telemetry.

Run:
    python tests/test_backend.py
"""

import io
import sys
from pathlib import Path

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image
from fastapi.testclient import TestClient
from backend.app import app


def make_test_leaf_image(color=(34, 139, 34), size=(256, 256)) -> bytes:
    """Create an in-memory JPEG test leaf image."""
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_verdix_system():
    client = TestClient(app)

    print("=" * 65)
    print("  RUNNING NOVAMIND INTEGRATION TEST SUITE")
    print("=" * 65)

    # ── 1. Health Endpoint (/api/health) ──────────────────────────────────
    print("\n─── 1. Health Check Endpoint (/api/health) ───")
    resp = client.get("/api/health")
    print(f"Status: {resp.status_code}  |  Body: {resp.json()}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    body = resp.json()
    assert body["status"] == "healthy"
    assert "model_loaded" in body
    assert "gemini_active" in body
    assert "total_classes" in body
    print("✓ /api/health passed")

    # ── 2. System Status Endpoint (/api/status) ───────────────────────────
    print("\n─── 2. System Status (/api/status) ───")
    resp = client.get("/api/status")
    print(f"Status: {resp.status_code}  |  Body: {resp.json()}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "online"
    print("✓ /api/status passed")

    # ── 3. Class List (/classes) ──────────────────────────────────────────
    print("\n─── 3. Class List (/classes) ───")
    resp = client.get("/classes")
    print(f"Status: {resp.status_code}")
    assert resp.status_code == 200
    classes = resp.json()["classes"]
    assert len(classes) == 38, f"Expected 38 classes, got {len(classes)}"
    assert "Tomato___Early_blight" in classes
    assert "Apple___Apple_scab" in classes
    print(f"✓ /classes returned all {len(classes)} PlantVillage classes")

    # ── 4. Main Diagnose Endpoint (/api/diagnose) ─────────────────────────
    print("\n─── 4. Main Diagnose Endpoint (/api/diagnose) ───")
    leaf_bytes = make_test_leaf_image(color=(40, 140, 40))
    resp = client.post(
        "/api/diagnose",
        files={"image": ("test_leaf.jpg", leaf_bytes, "image/jpeg")}
    )
    print(f"Status: {resp.status_code}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    data = resp.json()
    print(
        f"  name='{data.get('name')}' | score={data.get('score')} | "
        f"severity='{data.get('severity')}' | confidence={data.get('confidence')}"
    )
    assert "id" in data
    assert "name" in data
    assert "confidence" in data
    assert "score" in data
    assert "severity" in data
    assert "summary" in data
    assert isinstance(data.get("treatment"), list)
    assert isinstance(data.get("prevention"), list)
    print("✓ /api/diagnose passed")

    # ── 5. Pure Predict Endpoint (/api/predict) ───────────────────────────
    print("\n─── 5. Prediction Endpoint (/api/predict) ───")
    resp = client.post(
        "/api/predict",
        files={"file": ("test_leaf.jpg", leaf_bytes, "image/jpeg")}
    )
    print(f"Status: {resp.status_code}  |  Body keys: {list(resp.json().keys())}")
    assert resp.status_code in (200, 503)
    if resp.status_code == 200:
        pred_data = resp.json()
        assert "predicted_class" in pred_data
        assert "confidence" in pred_data
        assert "severity" in pred_data
        assert "heatmap_available" in pred_data
        print(f"✓ /api/predict returned valid prediction: {pred_data.get('predicted_class')}")
    else:
        print("⚠ /api/predict returned 503 (model standby in environment)")

    # ── 6. Gemini Agronomy Chatbot Endpoint (/api/chat) ───────────────────
    print("\n─── 6. Gemini Agronomy Chatbot (/api/chat) ───")
    chat_payload = {
        "message": "What is the recommended sanitation protocol for tomato early blight?",
        "history": [],
        "diagnosis_context": {
            "crop": "Tomato",
            "disease_name": "Tomato - Early Blight",
            "confidence": 0.92,
            "severity": "Moderate",
            "summary": "Dark concentric target lesions observed."
        }
    }
    resp = client.post("/api/chat", json=chat_payload)
    print(f"Status: {resp.status_code}")
    assert resp.status_code in (200, 503)
    if resp.status_code == 200:
        chat_data = resp.json()
        assert chat_data.get("success") is True
        assert len(chat_data.get("response", "")) > 20
        print(f"✓ /api/chat success with model: {chat_data.get('model_used')}")
        print(f"  Snippet: {chat_data.get('response')[:110]}...")
    else:
        print("⚠ /api/chat returned 503 (API key not configured in test environment)")

    # ── 7. Input Security: Non-image Rejection ────────────────────────────
    print("\n─── 7. Security: Invalid File Type Rejection ───")
    resp = client.post(
        "/api/diagnose",
        files={"image": ("malicious.exe", b"MZ\x90\x00\x03\x00fake binary", "application/octet-stream")}
    )
    print(f"Status: {resp.status_code} (expected 400)")
    assert resp.status_code == 400
    print("✓ Non-image rejection verified")

    # ── 8. Input Security: Empty File Rejection ───────────────────────────
    print("\n─── 8. Security: Empty File Rejection ───")
    resp = client.post(
        "/api/diagnose",
        files={"image": ("empty.jpg", b"", "image/jpeg")}
    )
    print(f"Status: {resp.status_code} (expected 400)")
    assert resp.status_code == 400
    print("✓ Empty file rejection verified")

    # ── 9. Field Telemetry (/api/field) ───────────────────────────────────
    print("\n─── 9. Field Health Telemetry (/api/field) ───")
    resp = client.get("/api/field")
    print(f"Status: {resp.status_code}  |  Body: {resp.json()}")
    assert resp.status_code == 200
    field_data = resp.json()
    assert "health" in field_data
    assert "alerts" in field_data
    assert "scans_week" in field_data
    assert "total" in field_data
    print("✓ /api/field passed")

    # ── 10. History Log (/api/history) ────────────────────────────────────
    print("\n─── 10. Scan History (/api/history) ───")
    resp = client.get("/api/history")
    print(f"Status: {resp.status_code}  |  Record count: {len(resp.json())}")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    print("✓ /api/history passed")

    # ── 11. Static Frontend Delivery (/) ──────────────────────────────────
    print("\n─── 11. Static Frontend Delivery (/) ───")
    resp = client.get("/")
    print(f"Status: {resp.status_code}")
    assert resp.status_code == 200
    assert "NovaMind" in resp.text
    assert "Gemini Agronomy Assistant" in resp.text
    print("✓ Frontend delivery verified (includes NovaMind dashboard & Gemini chatbot)")

    print("\n" + "=" * 65)
    print("  ALL 11 BACKEND & INTEGRATION TESTS PASSED ✓")
    print("=" * 65)


if __name__ == "__main__":
    test_verdix_system()
