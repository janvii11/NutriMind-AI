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
st.markdown("""
<style>

.stApp{
background:#FFFFFF !important;
}

.main{
background:#FFFFFF !important;
}

.block-container{
padding-top:2rem;
padding-bottom:2rem;
max-width:1200px;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<div style="background:linear-gradient(135deg,#F6FFF5,#ECF9EC,#DDF5D8);padding:45px;border-radius:28px;box-shadow:0 12px 30px rgba(46,125,50,.12);margin-bottom:30px;text-align:center;">

<div style="font-size:58px;margin-bottom:10px;">🍽</div>

<h1 style="color:#14532D;font-size:44px;font-weight:800;margin-bottom:12px;">
Meal Tracker
</h1>

<p style="font-size:18px;color:#4B6353;max-width:650px;margin:auto;line-height:1.7;">
 Monitor your daily meals, calories and nutrition progress with your personal AI meal journal.
</p>

</div>
""", unsafe_allow_html=True)
uid = get_uid()

if not uid:
    st.error("Please login again.")
    st.stop()

df = get_meals_dataframe(uid)

if not df.empty:
    st.markdown("""
    <h2 style="
    color:#14532D;
    font-weight:800;
    margin-bottom:20px;
    ">
    🍽 Today's Meals
    </h2>
    """, unsafe_allow_html=True)

    today = pd.Timestamp.today().strftime("%Y-%m-%d")
    today_df = df[df["Date"] == today]

    if len(today_df) == 0:
        st.info("No meals saved today.")
    else:

        for _, row in today_df.iterrows():

            html_card = (
            f'<div style="background:white;color:#1F2937;border-left:8px solid #43A047;'
            f'box-shadow:0 10px 25px rgba(46,125,50,.10);border-radius:22px;padding:18px;margin-bottom:12px;">'
            f'<h3 style="color:#14532D;margin-bottom:10px;font-weight:800;">🍽 {row["Meal_Type"]}</h3>'
            f'<p style="font-size:20px;font-weight:700;margin:8px 0;color:#1F2937;">{row["Food"].replace("_"," ").title()}</p>'

            f'<p style="color:#43A047;font-size:17px;font-weight:700;">🔥 {row["Calories"]} kcal</p>'
            f'</div>'
            )
            st.markdown(html_card, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <h2 style="
    color:#14532D;
    font-weight:800;
    ">
    📊 Today's Summary
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        html_meals = (
        f'<div style="background:#FFFFFF;border:1px solid #E3F2E5;padding:25px;'
        f'border-radius:22px;text-align:center;box-shadow:0 10px 25px rgba(46,125,50,.10);">'

        f'<h3 style="color:#43A047;">🍽 Total Meals</h3>'

        f'<h1 style="color:#14532D;">{len(df)}</h1>'

        f'</div>'
        )
        st.markdown(html_meals, unsafe_allow_html=True)

    with col2:
        html_calories = (
        f'<div style="background:#FFFFFF;border:1px solid #E3F2E5;padding:25px;'
        f'border-radius:22px;text-align:center;box-shadow:0 10px 25px rgba(46,125,50,.10);">'

        f'<h3 style="color:#43A047;">🔥 Calories</h3>'

        f'<h1 style="color:#14532D;">{df["Calories"].sum():.0f}</h1>'
        f'<p style="color:#6B7280;">kcal</p>'

        f'</div>'
        )
        st.markdown(html_calories, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <h2 style="
    color:#14532D;
    font-weight:800;
    ">
    📜 Meal History
    </h2>
    """, unsafe_allow_html=True)

    st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
    )
    st.divider()

    if st.button(
    "🗑 Reset Meal History",
    use_container_width=True
    ):

        delete_meals(uid)

        st.success("✅ Meal history deleted successfully!")

        st.rerun()

else:
    st.markdown("""
    <div style="
    background:#F6FFF5;
    padding:20px;
    border-left:6px solid #43A047;
    border-radius:18px;
    color:#166534;
    font-size:17px;
    font-weight:600;
    box-shadow:0 8px 18px rgba(46,125,50,.08);
    ">

    🥗 No meals saved today.

    </div>
    """, unsafe_allow_html=True)