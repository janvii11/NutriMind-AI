import streamlit as st
import pandas as pd
import os
from styles import load_css

load_css()

st.title("🍽 Meal Tracker")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_NAME = BASE_DIR / "data" / "meal_history.csv"

if os.path.exists(FILE_NAME):

    df = pd.read_csv(FILE_NAME)
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

        os.remove(FILE_NAME)

        st.success("✅ Meal history deleted successfully!")

        st.rerun()

else:

    st.info("No meals recorded yet.")