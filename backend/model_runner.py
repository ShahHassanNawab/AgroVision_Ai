"""
backend/model_runner.py
=======================
Deep Learning Model Runner for Plant Disease Classification.
Loads the trained MobileNetV2 model (plantvillage_mobilenet_93.h5) on 38 PlantVillage classes,
runs exact MobileNetV2 preprocessing [-1.0, 1.0], executes on-device inference,
computes true Grad-CAM saliency heatmaps via backpropagation, and estimates
defensible lesion severity via symptomatic foliar color segmentation.
"""

import os
import io
import json
import base64
import logging
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path

import numpy as np
from PIL import Image

from backend.disease_knowledge import get_disease_info

logger = logging.getLogger("ModelRunner")
logger.setLevel(logging.INFO)

# ─────────────────────────────────────────────────────────────────────────────
# Class labels — 38 standard PlantVillage classes
# ─────────────────────────────────────────────────────────────────────────────

def _load_class_names() -> List[str]:
    """Load class names from weights/class_names.json or root class_names.json."""
    base_dir = Path(__file__).resolve().parent.parent
    search_paths = [
        base_dir / "weights" / "class_names.json",
        base_dir / "class_names.json",
    ]
    for p in search_paths:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    names = json.load(f)
                if isinstance(names, list) and len(names) > 0:
                    logger.info(f"Loaded {len(names)} class names from {p.name}")
                    return names
            except Exception as e:
                logger.warning(f"Could not read {p}: {e}")
    return []


def _format_class_name(raw: str) -> Dict[str, Any]:
    """
    Format 'Tomato___Early_blight' into structured metadata:
    {raw_name, formatted_name, crop, condition, is_healthy}
    """
    if "___" in raw:
        crop_raw, cond_raw = raw.split("___", 1)
    else:
        crop_raw, cond_raw = raw, "Condition"

    crop = crop_raw.replace("_", " ").strip()
    condition = cond_raw.replace("_", " ").strip().title()
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
# Objective Severity Estimation via Foliar Lesion Color Segmentation
# ─────────────────────────────────────────────────────────────────────────────

def calculate_lesion_severity(image: Image.Image, is_healthy_class: bool = False) -> Tuple[float, str, str]:
    """
    Computes an objective foliar lesion severity percentage based on symptomatic
    tissue area segmentation (chlorotic and necrotic lesions vs healthy leaf blade).

    Returns:
        (severity_percentage: float 0-100,
         severity_label: 'Healthy' | 'Low' | 'Moderate' | 'Severe',
         severity_method: str)
    """
    if is_healthy_class:
        return 0.0, "Healthy", "classified_healthy_foliage"

    try:
        rgb_img = image.convert("RGB").resize((256, 256), Image.Resampling.BILINEAR)
        arr = np.array(rgb_img, dtype=np.float32)
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

        # Isolate leaf blade from extreme white / dark background
        total_intensity = r + g + b
        leaf_mask = (total_intensity > 35) & (total_intensity < 735)
        leaf_pixel_count = np.count_nonzero(leaf_mask)

        if leaf_pixel_count < 500:
            return 25.0, "Moderate", "default_insufficient_leaf_mask"

        # Symptomatic lesion criteria:
        # 1. Necrotic spots (brown/black tissue: r > 1.15 * g, or dark spots with low green)
        # 2. Chlorotic halos (yellowish tissue: high r & g with low b)
        necrosis = ((r > 1.18 * g) & (r > 60)) | ((r < 75) & (g < 75) & (b < 75))
        chlorosis = (r > 150) & (g > 150) & (b < 100) & (abs(r - g) < 40)
        lesion_mask = leaf_mask & (necrosis | chlorosis)

        lesion_pixels = np.count_nonzero(lesion_mask)
        raw_percentage = (lesion_pixels / leaf_pixel_count) * 100.0
        percentage = round(float(np.clip(raw_percentage, 0.0, 100.0)), 1)

        if percentage < 10.0:
            label = "Low"
        elif percentage < 35.0:
            label = "Moderate"
        else:
            label = "Severe"

        return percentage, label, "foliar_lesion_color_segmentation"
    except Exception as e:
        logger.warning(f"Lesion severity estimation error: {e}")
        return 20.0, "Moderate", "fallback_heuristic"


# ─────────────────────────────────────────────────────────────────────────────
# ModelRunner class
# ─────────────────────────────────────────────────────────────────────────────

class ModelRunner:
    """
    Safe cached model loader and inference engine.
    Loads plantvillage_mobilenet_93.h5 once at startup, executes inference,
    computes genuine Grad-CAM heatmaps, and estimates disease severity.
    """

    def __init__(self, weights_path: Optional[str] = None):
        self.weights_path: Optional[str] = weights_path
        self.model = None
        self.framework: Optional[str] = None
        self.model_loaded: bool = False
        self.class_names: List[str] = _load_class_names()
        self.target_size: Tuple[int, int] = (224, 224)
        self.gradcam_model = None

        self._find_and_load_model()

    def _candidate_paths(self) -> List[Path]:
        """Locate model weights candidate paths."""
        candidates = []
        if self.weights_path and Path(self.weights_path).exists():
            candidates.append(Path(self.weights_path))

        base_dir = Path(__file__).resolve().parent.parent
        weights_dir = base_dir / "weights"

        for directory in [weights_dir, base_dir]:
            if directory.is_dir():
                for ext in ["*.h5", "*.keras", "*.pth", "*.pt", "*.onnx", "*.tflite"]:
                    for f in directory.glob(ext):
                        if f not in candidates:
                            candidates.append(f)
        return candidates

    def _find_and_load_model(self):
        """Iterate through candidates and load the trained model."""
        candidates = self._candidate_paths()
        if not candidates:
            logger.warning("[ModelRunner] No weight files found in weights/ or project root.")
            return

        for path in candidates:
            ext = path.suffix.lower()
            try:
                if ext in (".h5", ".keras"):
                    self._load_keras(str(path))
                elif ext in (".pth", ".pt"):
                    self._load_pytorch(str(path))
                elif ext == ".onnx":
                    self._load_onnx(str(path))

                if self.model_loaded:
                    self.weights_path = str(path)
                    logger.info(f"[ModelRunner] Successfully loaded {self.framework} model: {path.name}")
                    return
            except Exception as e:
                logger.error(f"[ModelRunner] Could not load candidate {path.name}: {e}")

    def _load_keras(self, path: str):
        """Load Keras model with compile=False and prepare Grad-CAM extraction submodel."""
        try:
            import tensorflow as tf
            self.model = tf.keras.models.load_model(path, compile=False)
            self.framework = "TensorFlow/Keras"
            self.model_loaded = True

            # Prepare Grad-CAM submodel if possible
            self._setup_keras_gradcam(tf)
        except ImportError:
            # Check if standalone keras is available
            try:
                import keras
                self.model = keras.models.load_model(path, compile=False)
                self.framework = "Keras 3"
                self.model_loaded = True
            except Exception as e:
                logger.warning(f"Keras import or load failed: {e}")
        except Exception as e:
            logger.error(f"TensorFlow load_model failed: {e}")

    def _setup_keras_gradcam(self, tf):
        """
        Inspect the loaded Keras model and prepare a gradient-extractor model
        for genuine Grad-CAM generation.
        """
        try:
            # Model structure: Sequential with input_layer_1, mobilenetv2_1.00_224, global_avg_pool, etc.
            base_extractor = None
            for layer in self.model.layers:
                if "mobilenetv2" in layer.name.lower():
                    base_extractor = layer
                    break

            if base_extractor:
                # Find last conv layer inside the MobileNetV2 backbone (e.g. 'out_relu' or 'Conv_1')
                target_conv_name = None
                for inner_layer in reversed(base_extractor.layers):
                    if isinstance(inner_layer, (tf.keras.layers.Conv2D, tf.keras.layers.DepthwiseConv2D)) or "relu" in inner_layer.name or "conv" in inner_layer.name:
                        target_conv_name = inner_layer.name
                        break

                if target_conv_name:
                    logger.info(f"[ModelRunner] Target Grad-CAM convolutional layer: '{target_conv_name}'")
                    self._gradcam_conv_layer_name = target_conv_name
                    self._gradcam_base_layer = base_extractor
        except Exception as err:
            logger.warning(f"[ModelRunner] Grad-CAM setup notice: {err}")

    def _load_pytorch(self, path: str):
        import torch
        model = torch.load(path, map_location="cpu")
        if hasattr(model, "eval"):
            model.eval()
        self.model = model
        self.framework = "PyTorch"
        self.model_loaded = True

    def _load_onnx(self, path: str):
        import onnxruntime as ort
        self.model = ort.InferenceSession(path)
        self.framework = "ONNX"
        self.model_loaded = True

    # ─────────────────────────────────────────────────────────────────────────
    # Preprocessing
    # ─────────────────────────────────────────────────────────────────────────

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Exact MobileNetV2 training preprocessing:
        1. RGB conversion
        2. Bilinear resize to 224x224
        3. Float32 cast
        4. Normalize to [-1.0, 1.0] via (arr / 127.5) - 1.0
        5. Expand dims -> shape (1, 224, 224, 3)
        """
        img_rgb = image.convert("RGB")
        img_resized = img_rgb.resize(self.target_size, Image.Resampling.BILINEAR)
        arr = np.array(img_resized, dtype=np.float32)
        norm_arr = (arr / 127.5) - 1.0
        return np.expand_dims(norm_arr, axis=0)

    # ─────────────────────────────────────────────────────────────────────────
    # Genuine Grad-CAM Generation
    # ─────────────────────────────────────────────────────────────────────────

    def generate_gradcam(self, image: Image.Image, pred_index: int) -> Tuple[bool, str]:
        """
        Generates genuine Grad-CAM explainability heatmap by computing gradients
        of the predicted class with respect to the last convolutional layer.
        Resizes heatmap to original dimensions and overlays with Jet colormap.
        """
        if not self.model_loaded or self.framework != "TensorFlow/Keras":
            return False, ""

        try:
            import tensorflow as tf

            # Prepare input tensor
            input_tensor = tf.convert_to_tensor(self.preprocess_image(image))

            # Build multi-output model mapping input to [last_conv_output, predictions]
            base_model = getattr(self, "_gradcam_base_layer", None)
            conv_name = getattr(self, "_gradcam_conv_layer_name", None)

            if not base_model or not conv_name:
                return False, ""

            # Create an intermediate feature extractor for the conv layer
            target_conv_layer = base_model.get_layer(conv_name)

            # We create a gradient tape over the full model
            with tf.GradientTape() as tape:
                # Forward pass: extract features from backbone
                tape.watch(input_tensor)
                # To capture gradients from the inner conv layer of the nested model,
                # we construct a sub-model that outputs both the conv feature map and the final classification:
                conv_extractor = tf.keras.Model(
                    inputs=base_model.inputs,
                    outputs=[target_conv_layer.output, base_model.output]
                )
                conv_features, base_output = conv_extractor(input_tensor)
                tape.watch(conv_features)

                # Pass base_output through the remaining layers of the sequential model
                x = base_output
                for layer in self.model.layers:
                    if layer != base_model and not isinstance(layer, tf.keras.layers.InputLayer):
                        x = layer(x)
                predictions = x
                class_channel = predictions[:, pred_index]

            # Compute gradients of class score with respect to feature map
            grads = tape.gradient(class_channel, conv_features)
            if grads is None:
                return False, ""

            # Global average pool the gradients
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

            # Weight the feature map channels
            conv_features_val = conv_features[0]
            heatmap = conv_features_val @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)

            # ReLU on heatmap and normalize between 0 and 1
            heatmap = tf.maximum(heatmap, 0.0)
            max_val = tf.math.reduce_max(heatmap)
            if max_val > 0:
                heatmap = heatmap / max_val
            heatmap_np = heatmap.numpy()

            # Resize heatmap to match input leaf image size
            orig_w, orig_h = image.size
            heatmap_img = Image.fromarray(np.uint8(255 * heatmap_np)).resize(
                (orig_w, orig_h), Image.Resampling.BILINEAR
            )
            heatmap_norm = np.array(heatmap_img, dtype=np.float32) / 255.0

            # Jet-like colormap synthesis:
            # Blue (cold) -> Cyan -> Green -> Yellow -> Red (hot)
            r_col = np.clip(1.5 * heatmap_norm - 0.5, 0, 1)
            g_col = np.clip(1.0 - np.abs(heatmap_norm - 0.5) * 2.0, 0, 1)
            b_col = np.clip(1.0 - 1.5 * heatmap_norm, 0, 1)

            color_heatmap = np.stack([r_col * 255, g_col * 255, b_col * 255], axis=-1).astype(np.uint8)

            # Blend color heatmap (45%) with original image (55%)
            orig_rgb = np.array(image.convert("RGB"), dtype=np.float32)
            blended = np.uint8(orig_rgb * 0.55 + color_heatmap * 0.45)
            blended_img = Image.fromarray(blended)

            buf = io.BytesIO()
            blended_img.save(buf, format="JPEG", quality=88)
            b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            return True, f"data:image/jpeg;base64,{b64}"

        except Exception as e:
            logger.warning(f"[ModelRunner] Genuine Grad-CAM computation error: {e}")
            return False, ""

    # ─────────────────────────────────────────────────────────────────────────
    # Public predict API
    # ─────────────────────────────────────────────────────────────────────────

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """
        Executes end-to-end inference on the leaf image using the trained deep learning model.
        Returns structured diagnostic results including predictions, confidence,
        objective lesion severity, genuine Grad-CAM heatmap, and disease information.
        """
        if not self.model_loaded:
            logger.warning("[ModelRunner] predict() called but model is not loaded.")
            return {
                "success": False,
                "model_loaded": False,
                "framework": None,
                "predicted_class": None,
                "disease_name": None,
                "confidence": None,
                "class_probabilities": {},
                "top_predictions": [],
                "severity": None,
                "severity_percentage": None,
                "severity_method": None,
                "heatmap_available": False,
                "heatmap": "",
                "treatment": [],
                "prevention": [],
                "message": (
                    "Model weights not loaded. Ensure plantvillage_mobilenet_93.h5 is in weights/ "
                    "and deep learning libraries are installed."
                ),
            }

        try:
            # 1. Preprocess
            tensor = self.preprocess_image(image)

            # 2. Run inference
            if self.framework == "TensorFlow/Keras" or self.framework == "Keras 3":
                preds = self.model.predict(tensor, verbose=0)
                probabilities = preds[0]
            elif self.framework == "PyTorch":
                import torch
                t = torch.from_numpy(np.transpose(tensor, (0, 3, 1, 2))).float()
                with torch.no_grad():
                    out = self.model(t)
                    probabilities = torch.softmax(out, dim=1)[0].numpy()
            elif self.framework == "ONNX":
                tensor_chw = np.transpose(tensor, (0, 3, 1, 2))
                input_name = self.model.get_inputs()[0].name
                out = self.model.run(None, {input_name: tensor_chw})[0]
                exp = np.exp(out - out.max())
                probabilities = (exp / exp.sum())[0]
            else:
                raise ValueError(f"Unsupported framework: {self.framework}")

            # 3. Top prediction
            top_index = int(np.argmax(probabilities))
            confidence = float(probabilities[top_index])
            raw_class = self.class_names[top_index] if top_index < len(self.class_names) else f"Class_{top_index}"
            fmt = _format_class_name(raw_class)

            # 4. Top-5 predictions
            top5_indices = np.argsort(probabilities)[::-1][:5]
            top_predictions = []
            for idx in top5_indices:
                idx_raw = self.class_names[idx] if idx < len(self.class_names) else f"Class_{idx}"
                idx_fmt = _format_class_name(idx_raw)
                top_predictions.append({
                    "class": idx_raw,
                    "name": idx_fmt["formatted_name"],
                    "confidence": round(float(probabilities[idx]), 4),
                    "percentage": f"{round(float(probabilities[idx]) * 100, 2)}%",
                })

            # Full class probabilities dictionary
            class_probs = {
                (self.class_names[i] if i < len(self.class_names) else f"Class_{i}"): round(float(probabilities[i]), 4)
                for i in range(len(probabilities))
            }

            # 5. Objective Lesion Severity Assessment
            is_healthy = fmt["is_healthy"]
            sev_pct, sev_label, sev_method = calculate_lesion_severity(image, is_healthy_class=is_healthy)

            # 6. Genuine Grad-CAM
            gradcam_success, heatmap_data = self.generate_gradcam(image, top_index)

            # 7. Curated agronomic disease information
            disease_info = get_disease_info(raw_class)

            # Health index score (0-100): 100 for pristine healthy, reduced by lesion severity
            health_score = int(np.clip(100 - sev_pct, 10, 100)) if not is_healthy else 96

            return {
                "success": True,
                "model_loaded": True,
                "framework": self.framework,
                "predicted_class": raw_class,
                "disease_name": fmt["formatted_name"],
                "crop": fmt["crop"],
                "condition": fmt["condition"],
                "is_healthy": fmt["is_healthy"],
                "scientific_name": disease_info.get("scientific_name", "N/A"),
                "confidence": round(confidence, 4),
                "confidence_percentage": f"{round(confidence * 100, 2)}%",
                "class_probabilities": class_probs,
                "top_predictions": top_predictions,
                "score": health_score,
                "severity": sev_label,
                "severity_percentage": sev_pct,
                "severity_method": sev_method,
                "heatmap_available": gradcam_success,
                "heatmap": heatmap_data,
                "summary": (
                    f"Predicted {fmt['formatted_name']} with {round(confidence * 100, 1)}% model confidence. "
                    f"Lesion area estimation indicates {sev_label} severity ({sev_pct}% symptomatic foliage)."
                ),
                "treatment": disease_info.get("treatment", []),
                "prevention": disease_info.get("prevention", []),
                "symptoms": disease_info.get("symptoms", []),
                "precautions": disease_info.get("precautions", ""),
                "model_mode": "real_model",
            }

        except Exception as e:
            logger.error(f"[ModelRunner] Prediction failed: {e}")
            return {
                "success": False,
                "model_loaded": self.model_loaded,
                "framework": self.framework,
                "predicted_class": None,
                "disease_name": None,
                "confidence": None,
                "error": str(e),
                "heatmap_available": False,
                "heatmap": "",
            }
