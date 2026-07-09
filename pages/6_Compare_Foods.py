import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from nutrition import nutrition_df
from styles import load_css

load_css()
st.title("⚖️ Compare Foods")

food_list = sorted(nutrition_df["Food_Name"].tolist())

col1, col2 = st.columns(2)

with col1:
    food1 = st.selectbox(
        "Select First Food",
        food_list,
        key="food1"
    )

with col2:
    food2 = st.selectbox(
        "Select Second Food",
        food_list,
        key="food2"
    )

info1 = nutrition_df[nutrition_df["Food_Name"] == food1].iloc[0]
info2 = nutrition_df[nutrition_df["Food_Name"] == food2].iloc[0]
st.divider()

comparison = {
    "Nutrition": [
        "Calories",
        "Protein",
        "Carbs",
        "Fat",
        "Health Score"
    ],
    food1.replace("_"," ").title(): [
        info1["Calories"],
        info1["Protein"],
        info1["Carbs"],
        info1["Fat"],
        info1["Health_Score"]
    ],
    food2.replace("_"," ").title(): [
        info2["Calories"],
        info2["Protein"],
        info2["Carbs"],
        info2["Fat"],
        info2["Health_Score"]
    ]
}

st.dataframe(comparison, use_container_width=True)
if info1["Health_Score"] > info2["Health_Score"]:

    st.success(f"🏆 {food1.replace('_',' ').title()} is the healthier choice!")

elif info2["Health_Score"] > info1["Health_Score"]:

    st.success(f"🏆 {food2.replace('_',' ').title()} is the healthier choice!")

else:

    st.info("🤝 Both foods have the same Health Score.")