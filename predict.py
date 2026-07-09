import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "food_model.h5"
CLASS_PATH = BASE_DIR / "models" / "class_names.json"

model = load_model(MODEL_PATH)

with open(CLASS_PATH) as f:
    class_names = json.load(f)

def predict_food(img):
    """
    Takes a PIL Image and returns:
    food_name, confidence
    """

    img = img.convert("RGB")
    img = img.resize((224, 224))

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    prediction = model.predict(img_array, verbose=0)[0]

    top3_idx = prediction.argsort()[-3:][::-1]

    top3 = []

    for i in top3_idx:
        top3.append({
            "food": class_names[i],
            "confidence": float(prediction[i] * 100)
        })

    food = top3[0]["food"]
    confidence = top3[0]["confidence"]

    return food, confidence, top3
