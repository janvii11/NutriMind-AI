import streamlit as st
import json
import os
import pandas as pd
from PIL import Image
from pathlib import Path
logo = Image.open("asset/logo.png")
from predict import predict_food
from nutrition import get_nutrition
from meal_tracker import save_meal
from alternatives import get_alternatives
from styles import load_css

load_css()
st.set_page_config(
    page_title="NutriMind AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)
PROFILE_FILE = "user_profile.json"
BASE_DIR = Path(__file__).resolve().parent
MEAL_FILE = BASE_DIR / "data" / "meal_history.csv"

def load_profile():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    return {}

profile = load_profile()
today_meals = 0
today_calories = 0
today_protein = 0

if os.path.exists(MEAL_FILE):

    df = pd.read_csv(MEAL_FILE)

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"]).dt.date

    today = pd.Timestamp.today().date()

    today_df = df[df["Date"] == today]

    today_meals = len(df)

    today_calories = df["Calories"].sum()

    today_protein = df["Protein"].sum()
    st.markdown("""
    <div style="
    background: linear-gradient(135deg,#0F172A,#1E3A8A,#2563EB);
    padding:40px;
    border-radius:22px;
    text-align:center;
    margin-bottom:20px;
    box-shadow:0px 8px 25px rgba(0,0,0,0.35);
    ">

    <h1 style="color:white;font-size:50px;margin-bottom:8px;">
    🥗 NutriMind AI
    </h1>

    <h3 style="color:#E2E8F0;font-weight:400;">
    AI Powered Smart Food Recognition & Nutrition Intelligence Platform
    </h3>

    <p style="color:#CBD5E1;font-size:18px;">
    🍽 Identify Food • 📊 Track Nutrition • 🤖 AI Coach • ❤️ Live Health Insights
    </p>

    </div>
    """, unsafe_allow_html=True)
if profile:

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#0D47A1,#1976D2);
    padding:18px;
    border-radius:15px;
    color:white;
    text-align:center;
    font-size:24px;
    ">
    👋 Welcome <b>{profile['name']}</b>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🧮 BMI", profile.get("bmi", "-"))

    with c2:
        st.metric("🔥 BMR", profile.get("bmr", "-"))

    with c3:
        st.metric("🎯 Goal", profile.get("goal", "-"))

    with c4:
        remaining = max(
            profile.get("bmr", 1800) - today_calories
        )

        st.metric(
            "⚡ Remaining",
            f"{remaining:.0f} kcal"
        )

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🍽 Total Meals", today_meals)

with col2:
    st.metric("🔥 Total Calories", f"{today_calories:.0f} kcal")

with col3:
    st.metric("💪 Total Protein", f"{today_protein:.1f} g")

st.divider()

st.markdown("""
<h1 style='color:#1565C0;text-align:center;'>

🥗 Welcome to NutriMind AI

</h1>
""", unsafe_allow_html=True)

st.success("🚀 Choose any page from the sidebar to start your AI nutrition journey.")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div style="
    background:#1E3A5F;
    padding:25px;
    border-radius:18px;
    border-left:8px solid #42A5F5;
    height:260px;
    ">
    <h2>📷 Food Recognition</h2>

    ✔ AI Food Detection<br>
    ✔ Gemini Vision<br>
    ✔ Nutrition Analysis<br>
    ✔ Health Score<br>
    ✔ Meal Risk Analysis

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div style="
    background:#234F36;
    padding:25px;
    border-radius:18px;
    border-left:8px solid #66BB6A;
    height:260px;
    ">
    <h2>📊 Dashboard</h2>

    ✔ Daily Calories<br>
    ✔ Meal History<br>
    ✔ Goal Progress<br>
    ✔ Nutrition Insights

    </div>
    """, unsafe_allow_html=True)

st.divider()
with st.sidebar:

    st.markdown("""
    <div style="text-align:center;">
        <h2>🥗 NutriMind AI</h2>
        <p style="color:gray;">Healthy Eating with AI</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="
    background:#1565C0;
    padding:15px;
    border-radius:12px;
    text-align:center;
    color:white;
    font-weight:bold;
    ">

    🚀 AI Nutrition Platform

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 📌 Quick Navigation

    🏠 Home

    📷 Food Recognition

    👤 User Profile

    📊 Dashboard

    🍽 Meal Tracker

    🥗 Compare Foods
    """)

    st.divider()

    st.caption("Version 1.0")

st.markdown("""
<div style='text-align:center;color:gray;'>

Made with ❤️ using <b>TensorFlow • Gemini AI • Streamlit</b>

</div>
""", unsafe_allow_html=True)