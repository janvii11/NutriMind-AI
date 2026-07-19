import streamlit as st
st.set_page_config(
    page_title="NutriMind AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)
from styles import load_css

load_css()
import json
import os
import pandas as pd
from firebase_db import get_meals_dataframe, load_profile
from session_manager import get_uid
from PIL import Image
from pathlib import Path
logo = Image.open("asset/logo.png")
with st.sidebar:

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
uid = get_uid()
profile = {}

if uid:
    profile = load_profile(uid) or {}
today_meals = 0
today_calories = 0
today_protein = 0

if uid:
    df = get_meals_dataframe(uid)

    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"]).dt.date

        today = pd.Timestamp.today().date()

        today_df = df[df["Date"] == today]

        today_meals = len(today_df)
        today_calories = today_df["Calories"].sum()
        today_protein = today_df["Protein"].sum()
st.markdown("""
<div style="
background:linear-gradient(135deg,#F3FAF3,#E8F5E9,#DDF5D8);
padding:40px;
border-radius:25px;
box-shadow:0 10px 25px rgba(46,125,50,.10);
margin-bottom:25px;
">

<h1 style="
text-align:center;
color:#14532D;
font-size:50px;
font-weight:900;
">

🥗 NutriMind AI

</h1>

<p style="
text-align:center;
font-size:20px;
color:#355E3B;
">

Smart Food Recognition & Nutrition Intelligence Platform

</p>

<p style="
text-align:center;
font-size:17px;
color:#5B7A5E;
">

🍽 Identify Food • 📊 Analyze Nutrition • 🤖 AI Coach • ❤️ Stay Healthy

</p>

</div>
""", unsafe_allow_html=True)
if profile:

    st.markdown(f"""
    <div style="
    background:white;
    border-left:8px solid #43A047;
    box-shadow:0 8px 20px rgba(46,125,50,.08);  
    padding:18px;
    border-radius:15px;
    color:#14532D;
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
<h1 style='
text-align:center;
color:#14532D;
font-size:42px;
font-weight:900;
'>

🥗 Welcome to NutriMind AI

</h1>
""", unsafe_allow_html=True)

st.info("👈 Use the sidebar to explore Food Recognition, Dashboard, Meal Tracker and Profile.")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div style="
    background:white;
    border-left:8px solid #43A047;
    box-shadow:0 8px 20px rgba(46,125,50,.08);
    color:#14532D;
    padding:25px;
    border-radius:18px;
    height:260px;
    ">
    <h2>📷 Food Recognition</h2>

    ✔ AI Food Detection<br>
    ✔ AI Vision<br>
    ✔ Nutrition Analysis<br>
    ✔ Health Score<br>
    ✔ Meal Risk Analysis

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div style="
    background:white;
    border-left:8px solid #81C784;
    box-shadow:0 8px 20px rgba(46,125,50,.08);
    color:#14532D;
    padding:25px;
    border-radius:18px;
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
    background:linear-gradient(135deg,#43A047,#2E7D32);
    padding:15px;
    border-radius:12px;
    text-align:center;
    color:white;
    font-weight:bold;
    ">

    🚀 AI Nutrition Platform

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.caption("Version 1.0")

st.markdown("""
<div style='text-align:center;color:gray;'>

Made with ❤️ by Team NutriMind AI

TensorFlow • Firebase • Streamlit • AI

</div>
""", unsafe_allow_html=True)