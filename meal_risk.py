import streamlit as st
from firebase_db import load_profile


def meal_risk(info):

    uid = st.session_state.get("uid")

    if uid:
        profile = load_profile(uid)
    else:
        profile = {}
    if profile is None:
        profile = {}

    risk = 0

    reasons = []

    # Calories
    if info["Calories"] > 500:
        risk += 2
        reasons.append("High Calories")

    # Fat
    if info["Fat"] > 20:
        risk += 2
        reasons.append("High Fat")

    # Protein
    if info["Protein"] >= 20:
        risk -= 1
        reasons.append("Good Protein")

    # Health Score
    if info["Health_Score"] < 50:
        risk += 2
        reasons.append("Low Health Score")

    if profile:

        diseases = profile.get("disease", [])

        goal = profile.get("goal", "")

        if "Diabetes" in diseases and info["Carbs"] > 40:
            risk += 2
            reasons.append("High Carbs for Diabetes")

        if "PCOS" in diseases and info["Fat"] > 15:
            risk += 2
            reasons.append("High Fat for PCOS")

        if goal == "Weight Loss" and info["Calories"] > 400:
            risk += 2
            reasons.append("Too many Calories for Weight Loss")

    if risk <= 1:
        level = "LOW"

    elif risk <= 4:
        level = "MEDIUM"

    else:
        level = "HIGH"

    return level, reasons