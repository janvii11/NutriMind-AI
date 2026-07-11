import streamlit as st

if not st.session_state.get("logged_in"):
    st.warning("🔒 Please login first.")
    st.stop()
import streamlit as st
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from styles import load_css
from firebase_db import (
    get_meals_dataframe,
    delete_meals
)
from session_manager import get_uid
load_css()

st.title("🍽 Meal Tracker")
uid = get_uid()

if not uid:
    st.error("Please login again.")
    st.stop()

df = get_meals_dataframe(uid)

if not df.empty:
    st.subheader("🍽 Today's Meals")

    today = pd.Timestamp.today().strftime("%Y-%m-%d")
    today_df = df[df["Date"] == today]

    if len(today_df) == 0:
        st.info("No meals saved today.")
    else:

        for _, row in today_df.iterrows():

            st.markdown(f"""
            <div style="
                background-color:#262730;
                color:white;
                padding:18px;
                border-radius:15px;
                margin-bottom:12px;
                border-left:6px solid #4CAF50;
            ">
                <h4>{row['Meal_Type']} 🍽</h4>
                <b>{row['Food'].replace('_',' ').title()}</b><br>
                🔥 {row['Calories']} kcal
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📊 Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🍽 Total Meals", len(df))

    with col2:
        st.metric("🔥 Total Calories", f"{df['Calories'].sum():.0f} kcal")

    st.divider()

    st.subheader("🍽 Meal History")

    st.dataframe(df, use_container_width=True)
    st.divider()

    if st.button("🗑 Reset Meal History"):

        delete_meals(uid)

        st.success("✅ Meal history deleted successfully!")

        st.rerun()

else:
    st.info("🍽 No meals recorded yet.")