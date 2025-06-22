import onnxruntime as ort
import numpy as np
from PIL import Image
import os
import json

# Only load MobileNetV2 ONNX model from local file
MODEL_FILENAME = 'mobilenetv2-7.onnx'
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', MODEL_FILENAME))
LABELS_FILENAME = 'imagenet_labels.txt'
LABELS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', LABELS_FILENAME))

def get_mobilenetv2_onnx(model_path=MODEL_PATH):
    print('Loading ONNX model from:', model_path)
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"ONNX model file not found at {model_path}. Please ensure the file is present.")
    return model_path

def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB').resize((224, 224))
    img = np.array(img).astype(np.float32) / 255.0
    img = (img - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    return img.astype(np.float32)

# Load ImageNet class labels from local file only
def load_imagenet_labels(labels_path=LABELS_PATH):
    if not os.path.exists(labels_path):
        raise FileNotFoundError(f"ImageNet labels file not found at {labels_path}. Please ensure the file is present.")
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f if line.strip()]
    return labels

def predict_logo(image_path):
    model_path = get_mobilenetv2_onnx()
    ort_session = ort.InferenceSession(model_path)
    img = preprocess_image(image_path)
    outputs = ort_session.run(None, {ort_session.get_inputs()[0].name: img})
    probs = np.squeeze(outputs[0])
    top_idx = int(np.argmax(probs))
    confidence = float(probs[top_idx])
    labels = load_imagenet_labels()
    predicted_label = labels[top_idx] if top_idx < len(labels) else 'unknown'
    return predicted_label, confidence
