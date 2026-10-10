"""
backend/gemini_analyzer.py
==========================
Google Gemini Vision & Agronomy Chatbot integration for plant disease analysis.
Utilizes the official google-genai SDK with resilient multi-model fallback.
"""

import os
import io
import json
import base64
import re
from typing import Dict, Any, Optional, List
from PIL import Image
import requests
from dotenv import load_dotenv

load_dotenv()


class GeminiAnalyzer:
    """
    Google Gemini Vision API integration for plant disease analysis and conversational agronomy.

    Attempts the google-genai SDK first with automatic multi-model fallback,
    followed by direct HTTPS REST fallback if needed.
    """

    # High-speed multi-model cascade ordered from fastest active working models to resilient fallbacks
    _MODELS = [
        "gemini-3.1-flash-lite",
        "gemini-flash-lite-latest",
        "gemini-2.5-flash-lite",
        "gemini-flash-latest",
        "gemini-3.8-flash",
        "gemini-3.5-flash",
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = (api_key or os.getenv("GEMINI_API_KEY", "")).strip()
        self._working_model: Optional[str] = "gemini-3.1-flash-lite"

    def set_api_key(self, api_key: str):
        self.api_key = api_key.strip()

    def is_configured(self) -> bool:
        return bool(self.api_key and not self.api_key.lower().startswith("your_"))

    def _get_ordered_models(self) -> List[str]:
        """Returns the model cascade with the known working model at index 0."""
        models = list(self._MODELS)
        if self._working_model and self._working_model in models:
            models.remove(self._working_model)
            models.insert(0, self._working_model)
        return models

    # ─────────────────────────────────────────────────────────────────────────
    # Prompt builder for leaf image diagnosis
    # ─────────────────────────────────────────────────────────────────────────

    def _build_prompt(self, local_model_context: Optional[Dict[str, Any]] = None) -> str:
        prompt = """You are an expert Agricultural Plant Pathologist and Agronomist evaluating a plant leaf image.
Diagnose the leaf and respond ONLY with a valid JSON object matching the exact schema below.

JSON Schema:
{
  "name": "<Crop species - specific disease condition, or 'Crop (Healthy)'>",
  "confidence": <float between 0.50 and 0.99 representing diagnostic confidence>,
  "score": <integer 0-100: leaf health index — 100 = pristine healthy, 0 = completely defoliated/ruined>,
  "severity": "<'Low' | 'Moderate' | 'Severe'>",
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
- Return ONLY raw JSON — no markdown code fences, no comments, no conversational text.
- If the leaf is healthy: severity='Low', score >= 85, treatment = routine maintenance.
- If the leaf is diseased: estimate severity based on observable symptomatic lesion area ('Low', 'Moderate', or 'Severe').
- Treatments must include safe, practical agronomic controls and caution against pesticide misuse.
"""
        if local_model_context and local_model_context.get("predicted_class"):
            pred = local_model_context.get("disease_name") or local_model_context.get("predicted_class")
            conf = local_model_context.get("confidence", "N/A")
            prompt += (
                f"\nContext: An on-device MobileNetV2 deep learning classifier detected: '{pred}' "
                f"(model confidence: {conf}). Cross-examine visually and corroborate or refine this diagnosis."
            )
        return prompt

    # ─────────────────────────────────────────────────────────────────────────
    # API call strategies for image analysis
    # ─────────────────────────────────────────────────────────────────────────

    def _call_via_rest(self, img_bytes: bytes, prompt: str) -> Optional[str]:
        """Direct HTTPS REST call: fast, strict per-model timeout, no client-side retry lag."""
        b64_image = base64.b64encode(img_bytes).decode("utf-8")
        payload = {
            "contents": [{
                "parts": [
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_image}},
                    {"text": prompt},
                ]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "response_mime_type": "application/json",
            },
        }
        headers = {"Content-Type": "application/json"}

        # Try top candidate models with strict 6s timeout
        for model in self._get_ordered_models()[:3]:
            url = (
                f"https://generativelanguage.googleapis.com/v1beta/models/"
                f"{model}:generateContent?key={self.api_key}"
            )
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=6)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            text = parts[0].get("text", "")
                            if text:
                                print(f"[GeminiAnalyzer] REST success with {model}")
                                self._working_model = model
                                return text
                elif resp.status_code in (429, 503):
                    # Rate limit or temporary spike on this model: instantly try next candidate
                    print(f"[GeminiAnalyzer] REST {model} busy (HTTP {resp.status_code}), pivoting immediately...")
                else:
                    print(f"[GeminiAnalyzer] REST {model} HTTP {resp.status_code}")
            except Exception as req_err:
                print(f"[GeminiAnalyzer] REST {model} timeout/error: {req_err}")
        return None

    def _call_via_sdk(self, img_bytes: bytes, prompt: str) -> Optional[str]:
        """Secondary attempt via google-genai SDK if REST fails."""
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            for model_name in self._get_ordered_models()[:2]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[
                            types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                            prompt,
                        ],
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.2,
                        ),
                    )
                    if response and response.text:
                        print(f"[GeminiAnalyzer] SDK success with {model_name}")
                        self._working_model = model_name
                        return response.text
                except Exception as err:
                    print(f"[GeminiAnalyzer] SDK {model_name} warning: {err}")
                    continue
        except ImportError:
            pass
        except Exception as e:
            print(f"[GeminiAnalyzer] SDK initialization error: {e}")
        return None

    # ─────────────────────────────────────────────────────────────────────────
    # Response parsing
    # ─────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _strip_fences(text: str) -> str:
        """Strip markdown fences if model outputs ```json ... ```"""
        cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned.strip())
        return cleaned.strip()

    def _parse_response(self, raw: str) -> Optional[Dict[str, Any]]:
        try:
            cleaned = self._strip_fences(raw)
            # Find outermost JSON brackets if surrounded by commentary
            json_match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
            if json_match:
                cleaned = json_match.group(1)

            data = json.loads(cleaned)
            return {
                "name": str(data.get("name", "Unidentified Plant Condition")),
                "confidence": min(max(float(data.get("confidence", 0.90)), 0.0), 1.0),
                "score": int(max(0, min(100, data.get("score", 50)))),
                "severity": str(data.get("severity", "Moderate")),
                "summary": str(data.get("summary", "Analysis completed by Gemini Vision.")),
                "treatment": list(data.get("treatment", [
                    "Prune symptomatic leaves using sanitised shears.",
                    "Apply targeted protective treatments according to local agricultural guidelines.",
                    "Adjust irrigation to prevent foliar moisture stagnation.",
                ])),
                "prevention": list(data.get("prevention", [
                    "Ensure adequate sunlight and proper plant spacing.",
                    "Inspect crops weekly for early disease symptoms.",
                ])),
                "demo": False,
            }
        except Exception as e:
            print(f"[GeminiAnalyzer] JSON parse error: {e} | raw: {raw[:200]}")
            return None

    # ─────────────────────────────────────────────────────────────────────────
    # Fallback diagnosis when API is unconfigured
    # ─────────────────────────────────────────────────────────────────────────

    def _generate_fallback_diagnosis(
        self, local_model_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Provides realistic agronomic output if Gemini key is missing or offline."""
        pred_class = (local_model_context or {}).get("predicted_class")
        conf = (local_model_context or {}).get("confidence")

        from backend.disease_knowledge import get_disease_info

        if pred_class:
            info = get_disease_info(pred_class)
            is_healthy = info["is_healthy"]
            display_name = f"{info['crop']} - {info['condition']}" if not is_healthy else f"{info['crop']} (Healthy)"
            confidence = float(conf) if conf is not None else 0.88
            score = 92 if is_healthy else 48
            severity = info["severity_baseline"]
            summary = (
                f"On-device MobileNetV2 detected: {display_name}. "
                f"Symptom profile: {', '.join(info['symptoms'][:2])}."
            )
            treatment = info["treatment"]
            prevention = info["prevention"]
        else:
            display_name = "Tomato - Early Blight (Alternaria solani)"
            confidence = 0.87
            score = 45
            severity = "Moderate"
            summary = (
                "Dark concentric target-shaped lesions detected on foliage. "
                "Add GEMINI_API_KEY in .env for real-time generative agronomic reasoning."
            )
            treatment = [
                "Prune and destroy infected lower leaves with sterilized shears.",
                "Apply an approved copper fungicide or chlorothalonil spray following product labels.",
                "Water at the base of the stem in the morning to keep foliage dry."
            ]
            prevention = [
                "Maintain 60 cm spacing between plants for adequate airflow.",
                "Apply clean organic mulch to prevent spore splash from soil.",
                "Rotate solanaceous crops on a 3-year cycle."
            ]

        return {
            "name": display_name,
            "confidence": confidence,
            "score": score,
            "severity": severity,
            "summary": summary,
            "treatment": treatment,
            "prevention": prevention,
            "demo": True,
        }

    # ─────────────────────────────────────────────────────────────────────────
    # Public analyze() API
    # ─────────────────────────────────────────────────────────────────────────

    def analyze(
        self,
        image: Image.Image,
        local_model_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Analyze a leaf image via Gemini Vision with automatic model fallback."""
        # High-speed payload optimization: downscale large images for near-instant network transmission
        # Google Gemini Vision operates on 768-1024px internal tiles. Sending full 4K phone photos
        # wastes valuable seconds transferring megabytes of base64 over the wire.
        img_copy = image.copy().convert("RGB")
        max_dim = 800
        if max(img_copy.size) > max_dim:
            img_copy.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

        buf = io.BytesIO()
        img_copy.save(buf, format="JPEG", quality=82, optimize=True)
        img_bytes = buf.getvalue()

        if self.is_configured():
            prompt = self._build_prompt(local_model_context)

            # Try direct high-speed REST first (no hidden SDK retries, 6s timeout)
            raw = self._call_via_rest(img_bytes, prompt)
            if not raw:
                # Resilient SDK fallback if REST was unreachable
                raw = self._call_via_sdk(img_bytes, prompt)

            if raw:
                parsed = self._parse_response(raw)
                if parsed:
                    return parsed

        return self._generate_fallback_diagnosis(local_model_context)

    # ─────────────────────────────────────────────────────────────────────────
    # Conversational Agronomy Chatbot API (PHASE 7)
    # ─────────────────────────────────────────────────────────────────────────

    def _chat_via_rest(
        self,
        user_message: str,
        system_instructions: str,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Fast REST fallback for Chatbot interactions."""
        contents = []
        if history:
            for turn in history[-8:]:
                role = "user" if turn.get("role") == "user" else "model"
                content = turn.get("content", "")
                if content:
                    contents.append({
                        "role": role,
                        "parts": [{"text": content}]
                    })
        contents.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })

        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [{"text": system_instructions}]
            },
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 800,
            }
        }
        headers = {"Content-Type": "application/json"}

        for model in self._get_ordered_models()[:2]:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=7)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            text = parts[0].get("text", "")
                            if text:
                                self._working_model = model
                                return {
                                    "success": True,
                                    "response": text.strip(),
                                    "model_used": model,
                                }
            except Exception as e:
                print(f"[GeminiChat] REST {model} error: {e}")
        return None

    def chat(
        self,
        user_message: str,
        history: Optional[List[Dict[str, str]]] = None,
        diagnosis_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Chat with Gemini as an expert crop disease agronomy assistant.
        Retains context of the active leaf diagnosis session.
        """
        if not self.is_configured():
            return {
                "success": False,
                "response": (
                    "Gemini API key is not configured in .env. Please add GEMINI_API_KEY "
                    "to enable live crop pathology consultation."
                ),
                "model_used": None,
            }

        # Build system instruction / framing with context
        system_instructions = (
            "You are NovaMind's expert Agricultural Crop Pathology & Agronomy Assistant.\n"
            "Your role is to guide farmers, agronomists, and growers on plant health, "
            "diagnostics, crop management, and preventative agronomy.\n\n"
            "GUIDELINES:\n"
            "- Explain symptoms, causes, and treatments in clear, actionable, beginner-friendly terms.\n"
            "- Discuss cultural practices, irrigation, sanitation, biological controls, and chemical treatments.\n"
            "- Clarify that AI computer vision predictions are screening aids, not certified laboratory diagnoses.\n"
            "- Always instruct users to follow product label instructions, pre-harvest intervals, and local regulations.\n"
            "- Never guarantee that a fungicide or pesticide will eradicate a disease.\n"
            "- If the user asks about an unrelated topic, politely guide them back to agricultural and plant care topics.\n"
        )

        if diagnosis_context:
            disease = diagnosis_context.get("disease_name") or diagnosis_context.get("predicted_class") or diagnosis_context.get("disease") or "Unknown"
            conf = diagnosis_context.get("confidence")
            conf_str = f"{round(float(conf)*100, 1)}%" if conf else "N/A"
            sev = diagnosis_context.get("severity", "Moderate")
            crop = diagnosis_context.get("crop", "the crop")
            summary = diagnosis_context.get("summary", "") or diagnosis_context.get("advice", "")
            treatments = diagnosis_context.get("treatment") or diagnosis_context.get("treat", [])
            preventions = diagnosis_context.get("prevention") or diagnosis_context.get("prev", [])
            symptoms = diagnosis_context.get("symptoms", [])

            system_instructions += (
                f"\nACTIVE LEAF SCAN CONTEXT:\n"
                f"- Crop: {crop}\n"
                f"- Detected Condition: {disease}\n"
                f"- Model Confidence: {conf_str}\n"
                f"- Severity Assessment: {sev}\n"
                f"- Initial Assessment Summary: {summary}\n"
            )
            if treatments and isinstance(treatments, list):
                system_instructions += f"- Known Treatments: {', '.join(str(t) for t in treatments[:3])}\n"
            if preventions and isinstance(preventions, list):
                system_instructions += f"- Prevention Practices: {', '.join(str(p) for p in preventions[:2])}\n"
            if symptoms and isinstance(symptoms, list):
                system_instructions += f"- Typical Symptoms: {', '.join(str(s) for s in symptoms[:3])}\n"

            system_instructions += (
                f"Use this diagnosis as the direct context for follow-up questions from the user. "
                f"However, acknowledge that the prediction is an algorithmic assessment that should be verified in the field.\n"
            )

        # 1. First attempt via google-genai SDK using the ordered models
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)

            contents = []
            if history:
                for turn in history[-8:]:
                    role = turn.get("role", "user")
                    content = turn.get("content", "")
                    if role in ("user", "model", "assistant") and content:
                        api_role = "user" if role == "user" else "model"
                        contents.append(types.Content(
                            role=api_role,
                            parts=[types.Part.from_text(text=content)]
                        ))

            contents.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)]
            ))

            config = types.GenerateContentConfig(
                system_instruction=system_instructions,
                temperature=0.4,
                max_output_tokens=800,
            )

            for model_name in self._get_ordered_models()[:2]:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config=config,
                    )
                    if response and response.text:
                        self._working_model = model_name
                        return {
                            "success": True,
                            "response": response.text.strip(),
                            "model_used": model_name,
                        }
                except Exception as err:
                    print(f"[GeminiChat] SDK {model_name} attempt failed: {err}")
                    continue
        except Exception as e:
            print(f"[GeminiChat] SDK error: {e}")

        # 2. Resilient REST fallback if SDK failed
        rest_chat_result = self._chat_via_rest(user_message, system_instructions, history)
        if rest_chat_result:
            return rest_chat_result

        return {
            "success": False,
            "response": (
                "The Gemini Agronomy service is temporarily experiencing high demand (503 Service Unavailable). "
                "Please click Retry in a few moments."
            ),
            "model_used": None,
            "service_unavailable": True,
        }
