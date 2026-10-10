# 🌿 AgroVision AI • NovaMind Plant Intelligence Platform

AgroVision AI is a production-ready plant leaf disease diagnosis and agronomic intelligence platform. It pairs on-device deep learning (**MobileNetV2** with 38 PlantVillage disease classes), **Grad-CAM explainability heatmaps**, and **Google Gemini Vision** agronomic pathology into a unified web application.

---

## 🏛️ System Architecture

```text
┌────────────────────────────────────────────────────────┐
│               Frontend Interface (SPA)                 │
│  HTML5 + Vanilla CSS + ES6 JavaScript                  │
│  (Hosted on GitHub Pages / Static or FastAPI Backend)  │
└─────────────────────────▲──────────────────────────────┘
                          │ HTTP REST / JSON / Multipart
                          ▼
┌────────────────────────────────────────────────────────┐
│             FastAPI Backend Service (Python)           │
│  - /api/diagnose   : MobileNetV2 Inference + Grad-CAM  │
│  - /api/chat       : Gemini Agronomy Assistant         │
│  - /api/health     : Engine Status & Model Readiness   │
│  - /api/field      : 7-Day Field Health Telemetry      │
│  - /api/history    : Diagnosis Records Persistence     │
└────────────────────────────────────────────────────────┘
```

---

## ⚠️ Important: GitHub vs. Backend Deployment

* **GitHub / GitHub Pages** is a **static web host**. It serves HTML, CSS, and client-side JavaScript. It **cannot** run Python, Uvicorn, TensorFlow, or read `.env` secrets.
* If you host the frontend on GitHub Pages (`https://<username>.github.io/<repo>/`), you must connect it to a running backend API.

### How to Connect GitHub Pages to the Backend:
1. Open your GitHub Pages site.
2. In the sidebar under **Engine Status**, click **Configure Backend API** (or click the alert banner at the top).
3. Enter your live backend URL (e.g. `https://your-backend.onrender.com` or `http://127.0.0.1:8000`).
4. Click **Test & Save**. The app will verify `/api/health` and instantly connect.

---

## 🚀 Running Locally (Full Stack)

### Quick Start (Windows)
Double-click `START_BACKEND.bat` in the project root, or run:

```powershell
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Configure environment (add your GEMINI_API_KEY in .env)
copy .env.example .env

# 3. Launch unified server
python run.py
```

The application will be live at:
* **Web Application:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Interactive API Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Health Endpoint:** [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## ☁️ Free Backend Cloud Deployment (Render / Railway)

This repository includes deployment configurations (`Procfile` and `render.yaml`) for one-click deployment.

### Deploying on Render (Free Tier):
1. Create a free account at [render.com](https://render.com).
2. Click **New +** → **Web Service** → Connect your GitHub repository `ShahHassanNawab/AgroVision_Ai`.
3. Configure the settings:
   * **Runtime:** `Python 3`
   * **Build Command:** `pip install -r backend/requirements.txt`
   * **Start Command:** `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
4. Under **Environment Variables**, add:
   * `GEMINI_API_KEY` = *your Google Gemini API Key*
5. Click **Deploy Web Service**.
6. Copy your Render URL (e.g., `https://agrovision-ai.onrender.com`) and paste it into the frontend's **Configure Backend API** modal!

---

## 🧪 Testing

Run the automated integration test suite:

```powershell
python tests/test_backend.py
```
This tests all 11 core endpoints including TensorFlow inference, Grad-CAM generation, image validation, chatbot responses, and static file delivery.
