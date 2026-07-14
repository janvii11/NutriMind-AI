import streamlit as st
import sys
import time
from pathlib import Path
from PIL import Image
if not st.session_state.get("logged_in"):
    st.warning("🔒 Please login first.")
    st.stop()
sys.path.append(str(Path(__file__).resolve().parent.parent))
from predict import predict_food
from nutrition import get_nutrition
from gemini_food import predict_unknown_food
from ai_coach import get_ai_advice
from alternatives import get_alternatives
from firebase_db import save_meal
from portion import estimate_portion
from meal_risk import meal_risk
from session_manager import get_uid
from styles import load_css

load_css()

start = time.time()

st.markdown("""
<div style="
background:linear-gradient(135deg,#00416A,#1E88E5);
padding:30px;
border-radius:20px;
text-align:center;
color:white;
box-shadow:0px 10px 25px rgba(0,0,0,.25);
">

<h1>📷 AI Food Recognition</h1>

<h4>Upload a food image and let AI analyze it instantly.</h4>

</div>
""", unsafe_allow_html=True)

st.write("")
st.info("📸 Supported formats: JPG • JPEG • PNG")

uploaded_file = st.file_uploader(
    "Upload your food image",
    type=["jpg","jpeg","png"]
)

if uploaded_file is not None:

    img = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <h3 style='text-align:center;'>📷 Uploaded Image</h3>
        """, unsafe_allow_html=True)
        st.image(
            img,
            use_container_width=True
        ) 
    with st.spinner("🤖 AI is analyzing your food..."):
        food, confidence, top3 = predict_food(img)
    # ---------------- Gemini Fallback ----------------
        st.write("Food:", food)
        st.write("Confidence:", confidence)
        st.write("Top3:", top3)
    if confidence < 75:

        st.info("🤖 Low confidence detected. Using Gemini Vision...")

        result = predict_unknown_food(img)

        food = result["food_name"]
        confidence = 95

        info = {
            "Calories": result["calories"],
            "Protein": result["protein"],
            "Carbs": result["carbs"],
            "Fat": result["fat"],
            "Health_Score": result["health_score"],
            "Nutri_Score": result["nutri_score"]
        }

        gemini_used = True

    else:

        info = get_nutrition(food)

        portion = estimate_portion(confidence)

        info["Calories"] = round(info["Calories"] * portion)
        info["Protein"] = round(info["Protein"] * portion, 1)
        info["Carbs"] = round(info["Carbs"] * portion, 1)
        info["Fat"] = round(info["Fat"] * portion, 1)

        gemini_used = False
    with st.expander("🔍 Top 3 Predictions"):

        for item in top3:

            st.write(
                f"• {item['food'].replace('_',' ').title()} "
                f"({item['confidence']:.2f}%)"
            )
    st.subheader("🥇 Top AI Predictions")

    for i, pred in enumerate(top3):

        medal = ["🥇", "🥈", "🥉"][i]

        st.write(
            f"{medal} {pred['food'].replace('_',' ').title()} - {pred['confidence']:.2f}%"
        )

    st.divider()

    with col2:

        if gemini_used:

            st.markdown("""
            <div style="
            background:#6A1B9A;
            padding:15px;   
            border-radius:12px;
            color:white;
            text-align:center;
            font-size:18px;
            font-weight:bold;
            ">
            🤖 Gemini Vision Analysis
            </div>
            """, unsafe_allow_html=True)

            st.info("""
        Prediction Source : **Gemini AI**

        Reason : The uploaded food was not confidently recognized by the CNN model,
        so Gemini Vision analyzed the image automatically.
            """)

            st.write(f"Possible Food: **{food.replace('_',' ').title()}**")
            st.toast("Prediction Completed 🎉")

            st.write(f"Confidence: **{confidence:.2f}%**")

            st.info(
                "This food may not be present in the trained dataset. "
                "The prediction is only an estimate."
            )

            st.write("### 🍽 Choose Closest Food")

            options = [
                x["food"].replace("_", " ").title()
                for x in top3
            ]

            selected = st.selectbox(
                "Select Food",
                options,
                key="food_choice"
            )

            st.success(f"Selected : {selected}")
        else:
            st.markdown("""
            <div style="
            background:#1565C0;
            padding:15px;
            border-radius:12px;
            color:white;
            text-align:center;
            font-size:18px;
            font-weight:bold;
            ">
            🧠 Prediction by Deep Learning Model
            </div>
            """, unsafe_allow_html=True)

            st.info("""
        Prediction Source : **CNN (EfficientNet)**

        High confidence prediction from the trained food classification model.
            """)
        
        end = time.time()

        st.caption(
            f"⏱ Analysis Time : {end-start:.2f} sec"
        )
        st.markdown(f"""
        <div style="
        background:linear-gradient(135deg,#0F4C81,#0066CC);
        padding:25px;
        border-radius:20px;
        color:white;
        text-align:center;
        box-shadow:0px 8px 20px rgba(0,0,0,.25);
        ">

        <h2>🍽 {food.replace('_',' ').title()}</h2>

        <h3>Confidence : {confidence:.2f}%</h3>

        </div>
        """, unsafe_allow_html=True)

        if confidence >= 90:
            st.success(f"Confidence : {confidence:.2f}%")

        elif confidence >= 75:
            st.warning(f"Confidence : {confidence:.2f}%")

        else:
            st.error(f"Confidence : {confidence:.2f}%")
            st.info(f"🍽 Estimated Portion Size : {round(portion*100)}%")

        cards = [
            ("🔥 Calories", f"{info['Calories']} kcal", "#C62828"),
            ("💪 Protein", f"{info['Protein']} g", "#1565C0"),
            ("🍚 Carbs", f"{info['Carbs']} g", "#2E7D32"),
            ("🥑 Fat", f"{info['Fat']} g", "#EF6C00")
        ]

        cols = st.columns(4)

        for col, (title, value, color) in zip(cols, cards):

            with col:

                st.markdown(f"""
                <div style="
                background:{color};
                padding:18px;
                border-radius:16px;
                color:white;
                text-align:center;
                box-shadow:0px 8px 18px rgba(0,0,0,.25);
                ">
                <h4>{title}</h4>
                <h2>{value}</h2>
                </div>
                """, unsafe_allow_html=True)
        st.divider()

        st.markdown("## 🩺 Health Score")

        health_score = int(info["Health_Score"])

        if health_score >= 80:
            bg = "#2E7D32"
            status = "🟢 Excellent Choice"

        elif health_score >= 50:
            bg = "#F9A825"
            status = "🟡 Moderate Choice"

        else:
            bg = "#C62828"
            status = "🔴 Eat Occasionally"

        st.markdown(f"""
        <div style="
        background:{bg};
        padding:25px;
        border-radius:18px;
        text-align:center;
        color:white;
        box-shadow:0px 8px 18px rgba(0,0,0,.25);
        ">

        <h2>{health_score}/100</h2>

        <h3>{status}</h3>

        </div>
        """, unsafe_allow_html=True)

        with col2:

            grade = info["Nutri_Score"]

            colors = {
                "A":"#2E7D32",
                "B":"#43A047",
                "C":"#F9A825",
                "D":"#EF6C00",
                "E":"#C62828"
            }

            st.markdown(f"""
            <div style="
            background:{colors.get(grade, '#FFFFFF')};
            padding:25px;
            border-radius:18px;
            color:white;
            text-align:center;
            box-shadow:0px 8px 18px rgba(0,0,0,.25);
            ">

            <h2>🥗 Nutri Score</h2>

            <h1>{grade}</h1>

            </div>
            """, unsafe_allow_html=True)
        st.divider()

        st.markdown("## 💡 Healthier Alternatives")
        alternatives = get_alternatives(food)
        if alternatives:

            for alt in alternatives:
                st.success("✅ " + alt.replace("_", " ").title())


        st.divider()
        st.divider()

        st.subheader("🚦 AI Meal Risk Analysis")

        risk, reasons = meal_risk(info)

        if risk == "LOW":
            st.success("🟢 LOW RISK")

        elif risk == "MEDIUM":
            st.warning("🟡 MEDIUM RISK")

        else:
            st.error("🔴 HIGH RISK")

        for reason in reasons:
            st.write("✔", reason)

        st.markdown("## 🤖 AI Nutrition Coach")

        advice = get_ai_advice(food, info)

        for item in advice:
            st.info(item)
        st.divider()

        st.subheader("🍽 Save This Meal")

        meal_type = st.selectbox(
            "Select Meal Type",
            ["Breakfast", "Lunch", "Dinner", "Snacks"],
            key="meal_type_predict"
        )

        if st.button(
            "✅ Save Meal",
            key="save_meal_btn"
        ):
            uid = get_uid()

            if not uid:
                st.error("Please login again.")
                st.stop()

            if gemini_used:
                st.success(f"🤖 Gemini identified: {food}")
                st.info(result.get("advice", "No AI advice available."))
            save_meal(
                uid,
                food,
                info,
                meal_type
            )

            st.success("✅ Meal Saved Successfully!")
            st.balloons()

