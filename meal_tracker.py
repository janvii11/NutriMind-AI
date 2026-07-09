import pandas as pd
import os
from datetime import datetime
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = BASE_DIR / "data" / "meal_history.csv"

def save_meal(food, info, meal_type):

    meal = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Meal_Type": meal_type,
        "Food": food,
        "Calories": info["Calories"],
        "Protein": info["Protein"],
        "Carbs": info["Carbs"],
        "Fat": info["Fat"]
    }

    df = pd.DataFrame([meal])

    if os.path.exists(FILE_NAME):
        df.to_csv(FILE_NAME, mode="a", header=False, index=False)
    else:
        df.to_csv(FILE_NAME, index=False)

    print("✅ Meal saved successfully!")