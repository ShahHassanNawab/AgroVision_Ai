import time
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

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
        "maxOutputTokens": 280
    }
}
headers = {"Content-Type": "application/json"}

models = [
    "gemini-3.1-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-2.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest"
]

for m in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
    t0 = time.time()
    try:
        r = requests.post(url, json=payload_text, headers=headers, timeout=8)
        print(f"{m}: HTTP {r.status_code} in {time.time()-t0:.2f}s")
    except Exception as e:
        print(f"{m}: error {e} in {time.time()-t0:.2f}s")
