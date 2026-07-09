import streamlit as st
import pandas as pd
import os
import plotly.express as px
import json
import plotly.graph_objects as go
from styles import load_css

load_css()
st.markdown("""
<h1 style='text-align:center;
color:#00E5FF;
font-size:42px;'>
🥗 NutriMind AI Dashboard
</h1>

<p style='text-align:center;
font-size:18px;
color:gray;'>
Track • Analyze • Improve Your Nutrition
</p>
""", unsafe_allow_html=True)

st.divider()

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FILE_NAME = BASE_DIR / "data" / "meal_history.csv"
PROFILE_FILE = "user_profile.json"

def load_profile():
    try:
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}
if os.path.exists(FILE_NAME):

    df = pd.read_csv(FILE_NAME)
    profile = load_profile()

    bmr = profile.get("bmr", 1800)
    goal = profile.get("goal", "Maintain Weight")

    if goal == "Weight Loss":
        CALORIE_GOAL = int(bmr - 400)

    elif goal == "Weight Gain":
        CALORIE_GOAL = int(bmr + 400)

    elif goal == "Muscle Gain":
        CALORIE_GOAL = int(bmr + 250)

    else:
        CALORIE_GOAL = int(bmr)

    PROTEIN_GOAL = max(int(profile.get("weight", 60) * 1.2), 60)
    CARBS_GOAL = int(CALORIE_GOAL * 0.5 / 4)
    FAT_GOAL = int(CALORIE_GOAL * 0.25 / 9)
    # KPIs
    total_calories = df["Calories"].sum()
    total_meals = len(df)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#ff6a00,#ee0979);
            padding:25px;
            border-radius:18px;
            color:white;
            text-align:center;
            box-shadow:0px 8px 20px rgba(0,0,0,0.3);
        ">
            <h4>🔥 Total Calories</h4>
            <h1>{total_calories:.0f}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#00c6ff,#0072ff);
            padding:25px;
            border-radius:18px;
            color:white;
            text-align:center;
            box-shadow:0px 8px 20px rgba(0,0,0,0.3);
        ">
            <h4>🍽 Total Meals</h4>
            <h1>{total_meals}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Calories by Date
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    daily_calories = (
        df.groupby("Date", as_index=False)["Calories"]
        .sum()
        .sort_values("Date")
    )
    # Calories Chart

    if len(daily_calories) == 1:

        fig = px.bar(
            daily_calories,
            x="Date",
            y="Calories",
            text="Calories",
            title="📊 Today's Calories"
        )

        fig.update_traces(
            textposition="outside",
            marker_color="#00CC96"
        )

    else:

        fig = px.line(
            daily_calories,
            x="Date",
            y="Calories",
            markers=True,
            title="📈 Daily Calories Intake"
        )

        fig.update_traces(
            line=dict(width=4),
            marker=dict(size=10)
        )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Calories",
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    st.subheader("🥧 Meal Type Distribution")

    meal_counts = df["Meal_Type"].value_counts().reset_index()
    meal_counts.columns = ["Meal Type", "Count"]

    fig2 = px.pie(
        meal_counts,
        names="Meal Type",
        values="Count",
        hole=0.60,
        title="🥧 Meal Distribution"
    )

    fig2.update_traces(
        textposition="inside",
        textinfo="percent+label",
        pull=[0.05] * len(meal_counts),
        marker=dict(line=dict(color="white", width=2))
    )

    fig2.update_layout(
        template="plotly_dark",
        height=420,
        legend_title="Meal Type"
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.divider()

    st.subheader("📅 Today's Summary")

    today = pd.Timestamp.today().date()

    today_df = df[df["Date"] == today]

    calories = today_df["Calories"].sum()
    protein = today_df["Protein"].sum()
    carbs = today_df["Carbs"].sum()
    fat = today_df["Fat"].sum()

    meals = len(today_df)

    cards = [
        ("🍽 Meals", meals, "#667eea", "#764ba2"),
        ("🔥 Calories", f"{calories:.0f}", "#ff6a00", "#ee0979"),
        ("💪 Protein", f"{protein:.0f} g", "#11998e", "#38ef7d"),
        ("🍚 Carbs", f"{carbs:.0f} g", "#36D1DC", "#5B86E5"),
        ("🥑 Fat", f"{fat:.0f} g", "#f7971e", "#ffd200")
    ]

    cols = st.columns(5)

    for col, (title, value, c1, c2) in zip(cols, cards):

        with col:

            st.markdown(f"""
            <div style="
                background:linear-gradient(135deg,{c1},{c2});
                padding:18px;
                border-radius:16px;
                color:white;
                text-align:center;
                box-shadow:0 6px 15px rgba(0,0,0,.25);
            ">
                <h5>{title}</h5>
                <h2>{value}</h2>
            </div>
            """, unsafe_allow_html=True)
    st.divider()
    remaining = max(CALORIE_GOAL - calories, 0)

    st.subheader("🎯 Personalized Daily Goal")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("🔥 Daily Target", f"{CALORIE_GOAL} kcal")

    with c2:
        st.metric("⚡ Remaining Calories", f"{remaining} kcal")

    with c3:
        st.metric("🎯 Goal", goal)

    st.divider()
    

    st.subheader("🎯 Daily Goal Progress")

    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)


    def gauge(title, value, maximum, color):

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {"range": [0, maximum]},
                "bar": {"color": color},
                "bgcolor": "#EAEAEA"
            }
        ))

        fig.update_layout(
            height=260,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        return fig


    with c1:
        st.plotly_chart(
            gauge("🔥 Calories", calories, CALORIE_GOAL, "#FF6B6B"),
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            gauge("💪 Protein", protein, PROTEIN_GOAL, "#00C896"),
            use_container_width=True
        )

    with c3:
        st.plotly_chart(
            gauge("🍚 Carbs", carbs, CARBS_GOAL, "#4D96FF"),
            use_container_width=True
        )

    with c4:
        st.plotly_chart(
            gauge("🥑 Fat", fat, FAT_GOAL, "#FFC300"),
            use_container_width=True
        )
else:
    st.warning("🍽 No meals recorded yet.")

    st.markdown("""
    ### 🚀 Get Started

    1. Go to **Food Recognition**
    2. Upload a food image
    3. Click **Save Meal**
    4. Come back to Dashboard

    Your analytics will appear here automatically.
    """)