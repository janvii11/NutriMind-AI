import pandas as pd
# Load nutrition data only once
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "nutrition.csv"
nutrition_df = pd.read_csv(DATA_PATH)


def get_nutrition(food):
    """
    Returns the nutrition information of a food item.
    """

    food_info = nutrition_df[nutrition_df["Food_Name"] == food]

    if food_info.empty:
        return None

    return food_info.iloc[0]
if __name__ == "__main__":
    info = get_nutrition("pakode")

    print(info)
food_list = sorted(nutrition_df["Food_Name"].tolist())