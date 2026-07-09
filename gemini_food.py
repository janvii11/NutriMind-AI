import os
import json
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def predict_unknown_food(img):

    prompt = """
You are a nutrition expert.

Analyze this food image.

Return ONLY valid JSON.

{
    "food_name":"",
    "calories":0,
    "protein":0,
    "carbs":0,
    "fat":0,
    "health_score":0,
    "nutri_score":"",
    "advice":""
}

Rules:
- Identify the food.
- Estimate one serving.
- Calories should be realistic.
- Protein, carbs and fat should also be realistic.
- Health score should be between 0-100.
- Nutri score should be A/B/C/D/E.
- Return ONLY JSON.
"""

    response = model.generate_content([prompt, img])

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)
if __name__ == "__main__":

    img = Image.open(r"C:\Users\Janvi\Desktop\nmai\datasset\food\Food Classification\WhatsApp Image 2026-07-04 at 9.41.00 AM.jpeg")

    result = predict_unknown_food(img)

    print(result)