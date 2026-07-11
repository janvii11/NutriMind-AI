from gemini_food import model
import json

def get_alternatives(food):

    prompt = f"""
Suggest ONLY 3 healthier alternatives for {food}.

Return ONLY valid JSON.

Example:

{{
  "alternatives":[
    "Chapati",
    "Vegetable Salad",
    "Grilled Paneer"
  ]
}}

Do not write explanation.
Do not write markdown.
Do not use ```json.
"""

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        # remove markdown if Gemini adds it
        text = text.replace("```json", "")
        text = text.replace("```", "")

        data = json.loads(text)

        return data.get("alternatives", [])

    except Exception as e:

        print("Alternative Error:", e)

        print(response.text)

        return []