import tensorflow as tf
import numpy as np
import cv2
from PIL import Image

MODEL_PATH = "model.keras"

model = tf.keras.models.load_model(MODEL_PATH)

CLASS_NAMES = ["electricity", "fire", "garbage", "not_issue", "road", "water"]

def classify_image(image_file):
    # Load image
    img = Image.open(image_file).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Prediction
    preds = model.predict(img_array)
    confidence = float(np.max(preds))
    category = CLASS_NAMES[np.argmax(preds)]

    # Edge detection (for preview)
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    # Optional note
    note = "AI detected issue"
    if category == "not_issue":
        note = "⚠️ No issue detected"

    # ✅ IMPORTANT: ALWAYS RETURN 4 VALUES
    return category, round(confidence, 3), note, edges