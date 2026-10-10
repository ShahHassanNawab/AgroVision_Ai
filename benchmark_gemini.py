import time
import os
import base64
import io
import json
from dotenv import load_dotenv
import requests
from PIL import Image

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

img = Image.new("RGB", (800, 800), color=(34, 139, 34))
buf = io.BytesIO()
img.save(buf, format="JPEG", quality=82)
img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

prompt_with_image = """You are an expert Agricultural Plant Pathologist and Agronomist evaluating a plant leaf image.
Diagnose the leaf and respond ONLY with a valid JSON object matching the exact schema below.

JSON Schema:
{
  "name": "<Crop species - specific disease condition, or 'Crop (Healthy)'>",
  "confidence": 0.95,
  "score": 80,
  "severity": "Moderate",
  "summary": "<1-2 concise sentences summarizing observed symptoms, pathogens, and environmental risks>",
  "treatment": [
    "<Actionable treatment step 1>",
    "<Actionable treatment step 2>",
    "<Actionable treatment step 3>"
  ],
  "prevention": [
    "<Preventative cultural practice 1>",
    "<Preventative sanitation/irrigation practice 2>"
  ]
}
Rules:
- Return ONLY raw JSON — no markdown code fences, no comments.
Context: An on-device MobileNetV2 deep learning classifier detected: 'Tomato - Early Blight' (model confidence: 0.92)."""

payload_img = {
    "contents": [{
        "parts": [
            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}},
            {"text": prompt_with_image}
        ]
    }],
    "generationConfig": {"temperature": 0.2, "response_mime_type": "application/json"}
}

# Concise prompt sending only necessary info: predicted disease, confidence score, crop context
prompt_text_only = """You are an agricultural pathologist.
Plant: Tomato
Condition: Early Blight
Confidence: 92%

Provide concise agricultural advice in JSON:
{
  "summary": "1-2 sentences explaining symptoms and causes",
  "treatment": ["step 1", "step 2", "step 3"],
  "prevention": ["practice 1", "practice 2"]
}"""

payload_text = {
    "contents": [{"parts": [{"text": prompt_text_only}]}],
    "generationConfig": {
        "temperature": 0.2,
        "response_mime_type": "application/json",
        "maxOutputTokens": 300
    }
}

headers = {"Content-Type": "application/json"}

for model in ["gemini-3.1-flash-lite", "gemini-2.5-flash-lite"]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    # 1. Original (Image + Uncapped tokens)
    t0 = time.time()
    r1 = requests.post(url, json=payload_img, headers=headers, timeout=15)
    t_img = time.time() - t0
    
    # 2. Optimized (Text only + concise prompt + maxOutputTokens)
    t0 = time.time()
    r2 = requests.post(url, json=payload_text, headers=headers, timeout=15)
    t_text = time.time() - t0
    
    print(f"{model}:")
    print(f"  Original (with image, unbounded tokens): {t_img:.2f}s (HTTP {r1.status_code})")
    print(f"  Optimized (text-only, concise, token-capped): {t_text:.2f}s (HTTP {r2.status_code})")
    if r2.status_code == 200:
        print("  Sample text output:", r2.json()['candidates'][0]['content']['parts'][0]['text'][:120])
