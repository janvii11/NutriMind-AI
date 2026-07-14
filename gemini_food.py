import os
import json
import traceback
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.5-flash")


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
"""

    try:

        response = model.generate_content([prompt, img])
        print(response.text)
        text = response.text.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")

        return json.loads(text)

    

    except Exception as e:
        print("=" * 50)
        print(type(e))
        print(e)
        traceback.print_exc()
        print("=" * 50)

        return {
        "food_name": "Unknown Food",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "health_score": 0,
        "nutri_score": "N/A",
        "advice": "AI unavailable."
    }

        