"""
run.py — NovaMind / Verdix Plant Intelligence Platform Launcher
==============================================================
Pre-flight checks then starts the FastAPI server via uvicorn.

Usage:
    python run.py
"""

import os
import sys
from pathlib import Path


def _check_dependencies() -> list[str]:
    """Return a list of missing critical packages."""
    missing = []
    for pkg, import_name in [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("PIL", "Pillow"),
        ("numpy", "numpy"),
        ("dotenv", "python-dotenv"),
    ]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(import_name)
    return missing


def main():
    base_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(base_dir))

    # Reconfigure stdout for UTF-8 (Windows compatibility)
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 62)
    print("  NovaMind — Plant Intelligence Platform")
    print("=" * 62)

    # ── 1. Dependency check ──────────────────────────────────────────────
    missing_pkgs = _check_dependencies()
    if missing_pkgs:
        print(f"\n[ERROR] Missing packages: {', '.join(missing_pkgs)}")
        print("        Run:  pip install -r backend/requirements.txt\n")
        sys.exit(1)

    # ── 2. TensorFlow availability ───────────────────────────────────────
    try:
        import tensorflow as tf
        tf_ver = tf.__version__
        print(f"[TensorFlow]   ✓  version {tf_ver}")
    except ImportError:
        print("[TensorFlow]   !  Not installed. Model inference will be disabled.")
        print("               Run:  pip install tensorflow")

    # ── 3. Gemini API key ────────────────────────────────────────────────
    env_file = base_dir / ".env"
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("GEMINI_API_KEY="):
                    val = line.strip().split("=", 1)[1].strip()
                    if val and not val.lower().startswith("your_"):
                        gemini_key = val

    if gemini_key:
        print("[Gemini API]   ✓  API key detected — live Gemini Vision enabled")
    else:
        print("[Gemini API]   ⚠  No key found in .env — running in fallback/demo mode")
        print('               Add your key: GEMINI_API_KEY=AIza... in .env')

    # ── 4. Model weights ─────────────────────────────────────────────────
    weights_dir = base_dir / "weights"
    weight_files = (
        list(weights_dir.glob("*.h5"))
        + list(weights_dir.glob("*.keras"))
        + list(weights_dir.glob("*.pth"))
        + list(weights_dir.glob("*.pt"))
        + list(weights_dir.glob("*.onnx"))
        + list(weights_dir.glob("*.tflite"))
    )
    # Also check root directory
    root_weights = (
        list(base_dir.glob("*.h5"))
        + list(base_dir.glob("*.keras"))
    )
    all_weights = weight_files + [w for w in root_weights if w not in weight_files]

    if all_weights:
        print(f"[Model Weights] ✓  {len(all_weights)} weight file(s) found:")
        for wf in all_weights:
            size_mb = wf.stat().st_size / (1024 * 1024)
            print(f"                   {wf.name}  ({size_mb:.1f} MB)")
    else:
        print("[Model Weights] ⚠  No weight files found in weights/ or project root.")
        print("               Place plantvillage_mobilenet_93.h5 in the weights/ directory.")

    # ── 5. Class names ───────────────────────────────────────────────────
    class_json = next(
        (
            p for p in [base_dir / "weights" / "class_names.json", base_dir / "class_names.json"]
            if p.exists()
        ),
        None,
    )
    if class_json:
        import json
        with open(class_json) as f:
            n = len(json.load(f))
        print(f"[Class Names]   ✓  {n} classes loaded from {class_json.name}")
    else:
        print("[Class Names]   ⚠  class_names.json not found.")

    print("-" * 62)
    print("[Server]        Starting at  http://127.0.0.1:8000")
    print("                Docs UI at   http://127.0.0.1:8000/docs")
    print("                App UI at    http://127.0.0.1:8000/")
    print("=" * 62)

    import uvicorn
    uvicorn.run(
        "backend.app:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("DEBUG", "true").lower() == "true",
    )


if __name__ == "__main__":
    main()
