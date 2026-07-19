import streamlit as st
import sys
import time
from pathlib import Path
from PIL import Image
# ---------------- LOGIN CHECK ---------------- #
if not st.session_state.get("logged_in"):
    st.warning("🔒 Please login first.")
    st.stop()
# ---------------- IMPORTS ---------------- #
sys.path.append(str(Path(__file__).resolve().parent.parent))
from predict import predict_food
from nutrition import get_nutrition
from gemini_food import predict_unknown_food
from ai_coach import get_ai_advice
from alternatives import get_alternatives
from food_alternatives import ALTERNATIVES
from firebase_db import save_meal
from portion import estimate_portion
from meal_risk import meal_risk
from session_manager import get_uid
from styles import load_css
load_css()
start = time.time()
# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="NutriMind AI",
    page_icon="🥗",
    layout="wide"
)
# ==========================================================
# NUTRIMIND V2 THEME - PISTACHIO EMERALD
# ==========================================================

st.markdown("""
<style>
.stApp{
background:#FAFCFA;
}


.block-container{

padding-top:2rem;
padding-bottom:2rem;

}


/* HERO */

.hero{

background:linear-gradient(
135deg,
#FCFFFC,
#F3FBF3,
#E7F6E7
);
padding:45px;

border-radius:30px;

box-shadow:
0 8px 25px rgba(22,101,52,.08);

margin-bottom:30px;

border:1px solid #DDEFD9;

}


.hero h1{

color:#166534;

font-size:46px;

font-weight:900;

letter-spacing:1px;

}


.hero p{

font-size:19px;

color:#64748B;

line-height:1.6;

}


/* UPLOAD BOX */


.upload-card{

background:white;

padding:28px;

border-radius:25px;

box-shadow:
0 8px 25px rgba(0,0,0,0.08);

border-left:
6px solid #6FBF73;

margin-top:20px;

}


.upload-card h3{

color:#166534;

font-weight:800;

}


</style>

""", unsafe_allow_html=True)
st.markdown("""

<div class="hero">

<h1>🥗 NutriMind AI</h1>

<p>
Your AI-powered nutrition companion.
Recognize food, analyze health impact,
track meals and get personalized diet insights.
</p>
</div>

""", unsafe_allow_html=True)
# ==========================================================
# UPLOAD CARD
# ==========================================================

st.markdown("""
<div class="upload-card">

<h2 style="
color:#166534;
font-weight:800;
margin-bottom:8px;
">
📷 Upload Your Food
</h2>

<p style="
font-size:16px;
color:#64748B;
margin-bottom:20px;
">
Take a clear picture or upload an image to receive an instant nutrition report.
</p>

<div style="
display:inline-block;
padding:8px 18px;
background:#EAF8EA;
color:#2E7D32;
border-radius:30px;
font-weight:700;
">
JPG • JPEG • PNG
</div>

</div>
""", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Choose an Image",
    type=["jpg","jpeg","png"],
    label_visibility="collapsed"
)
if uploaded_file is not None:

    img = Image.open(uploaded_file)

    left, right = st.columns([1, 1.15], gap="large")

    with left:

        st.markdown("""
        <div style="
        background:white;
        padding:20px;
        border-radius:22px;
        box-shadow:0 8px 25px rgba(0,0,0,.08);
        ">
        <h3 style="color:#2E7D32;text-align:center;">
        📷 Uploaded Image
        </h3>
        """, unsafe_allow_html=True)

        st.image(
            img,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with st.spinner("🥗 NutriMind AI is analyzing your meal..."):

        food, confidence, top3 = predict_food(img)

    # ------------------------------------------------
    # AI FALLBACK
    # ------------------------------------------------

    if confidence < 75:

        st.info("🤖 Low confidence detected. Running AI Vision...")

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

        info["Protein"] = round(info["Protein"] * portion,1)

        info["Carbs"] = round(info["Carbs"] * portion,1)

        info["Fat"] = round(info["Fat"] * portion,1)

        gemini_used = False

    # ------------------------------------------------

    with right:

        if gemini_used:

            bg = "linear-gradient(135deg,#166534,#4ADE80)"

            title = "🤖 AI Vision Prediction"

            desc = "Food analyzed using intelligent vision because confidence was low."

        else:

            bg = "linear-gradient(135deg,#064E3B,#10B981)"

            title = "🧠 Deep Learning Prediction"

            desc = "Prediction generated using NutriMind EfficientNet Model."
        st.markdown(f"""
        <div style="
        background:white;
        padding:35px;
        border-radius:28px;
        border:1px solid #E5F3E5;
        box-shadow:0 10px 25px rgba(34,139,34,.08);
        text-align:center;
        ">

        <div style="
        display:inline-block;
        background:#EAF8EA;
        color:#166534;
        padding:8px 20px;
        border-radius:30px;
        font-weight:700;
        margin-bottom:18px;
        ">

        {title}

        </div>

        <h1 style="
        color:#14532D;
        font-size:34px;
        font-weight:800;
        margin-bottom:10px;
        ">
        🍽 {food.replace('_',' ').title()}
        </h1>

        <h2 style="
        color:#6FBF73;
        font-weight:700;
        margin-bottom:18px;
        ">
        {confidence:.2f}% Confidence
        </h2>

        <p style="
        color:#64748B;
        font-size:16px;
        ">

        {desc}

        </p>

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if confidence >= 90:

            st.success("✅ Excellent Confidence")

        elif confidence >= 75:

            st.warning("⭐ Good Confidence")

        else:

            st.error("⚠ Estimated Prediction")

        end = time.time()

        st.caption(
            f"⏱ Analysis completed in {end-start:.2f} seconds"
        )

    # ------------------------------------------------

    st.markdown("""
    <h2 style="
    color:#14532D;
    font-weight:800;
    margin-top:25px;
    margin-bottom:18px;
    ">
    🏆 Top Predictions
    </h2>
    """, unsafe_allow_html=True)

    cols = st.columns(3)

    medals = ["🥇","🥈","🥉"]

    for col, pred, medal in zip(cols, top3, medals):

        with col:

            st.markdown(f"""
            <div style="
            background:linear-gradient(135deg,#FFFFFF,#F8FFF7);
            padding:28px;
            border-radius:22px;
            text-align:center;
            border:2px solid #C8E6C9;
            box-shadow:0 12px 25px rgba(46,125,50,.12);
            transition:0.3s;
            ">

            <div style="font-size:38px;">
            {medal}
            </div>

            <h3 style="
            color:#14532D;
            font-weight:800;
            margin-top:10px;
            ">
            {pred['food'].replace('_',' ').title()}
            </h3>

            <div style="
            display:inline-block;
            margin-top:10px;
            background:#2E7D32;
            color:white;
            padding:8px 18px;
            border-radius:30px;
            font-weight:700;
            font-size:17px;
            ">
            {pred['confidence']:.2f}%
            </div>

            </div>
            """, unsafe_allow_html=True)

    st.divider()
    with right:

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
            🤖 AI Vision Analysis
            </div>
            """, unsafe_allow_html=True)

            st.info("""
        Prediction Source : **AI**

        Reason : The uploaded food was not confidently recognized by the CNN model,
        so AI Vision analyzed the image automatically.
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
        

        if confidence >= 90:
            st.success(f"Confidence : {confidence:.2f}%")

        elif confidence >= 75:
            st.warning(f"Confidence : {confidence:.2f}%")

        else:
            st.error(f"Confidence : {confidence:.2f}%")
            st.info(f"🍽 Estimated Portion Size : {round(portion*100)}%")

        cards = [
            ("🔥", "Calories", f"{info['Calories']} kcal"),
            ("💪", "Protein", f"{info['Protein']} g"),
            ("🍚", "Carbs", f"{info['Carbs']} g"),
            ("🥑", "Fat", f"{info['Fat']} g")
        ]

        cols = st.columns(4)

        for col, (icon, title, value) in zip(cols, cards):

            with col:

                st.markdown(f"""
                <div style="
                background:white;
                border-radius:22px;
                padding:22px;
                border:1px solid #E6F4E6;
                text-align:center;
                box-shadow:0 6px 18px rgba(34,139,34,.08);
                ">

                <div style="
                font-size:32px;
                margin-bottom:10px;
                ">
                {icon}
                </div>

                <div style="
                color:#6B7280;
                font-size:15px;
                ">
                {title}
                </div>

                <div style="
                color:#166534;
                font-size:28px;
                font-weight:800;
                margin-top:8px;
                ">
                {value}
                </div>

                </div>
                """, unsafe_allow_html=True)
        st.divider()
# HEALTH & NUTRI SCORE

        st.markdown("## 🌿 Health Analysis")

        left_score, right_score = st.columns(2, gap="large")

        # ---------------- HEALTH SCORE ---------------- #

        with left_score:

            score = int(info["Health_Score"])

            if score >= 80:
                color = "#2E7D32"
                status = "Excellent"

            elif score >= 50:
                color = "#F9A825"
                status = "Moderate"

            else:
                color = "#D32F2F"
                status = "Needs Improvement"

            st.markdown(f"""
            <div style="
            background:white;
            border-radius:25px;
            padding:35px;
            text-align:center;
            border:1px solid #E7F5E8;
            box-shadow:0 8px 22px rgba(0,0,0,.08);
            ">

            <h3 style="color:#166534;">
            💚 Health Score
            </h3>

            <div style="
            width:130px;
            height:130px;
            margin:auto;
            border-radius:50%;
            border:10px solid {color};
            display:flex;
            justify-content:center;
            align-items:center;
            font-size:34px;
            font-weight:800;
            color:{color};
            margin-top:20px;
            margin-bottom:20px;
            ">

            {score}

            </div>

            <h4 style="color:#555;">
            {status}
            </h4>

            </div>
            """, unsafe_allow_html=True)

# ---------------- NUTRI SCORE ---------------- #

        with right_score:

            grade = info["Nutri_Score"]

            colors = {
                "A":"#2E7D32",
                "B":"#66BB6A",
                "C":"#F9A825",
                "D":"#EF6C00",
                "E":"#D32F2F"
            }

            st.markdown(f"""
            <div style="
            background:white;
            border-radius:25px;
            padding:35px;
            text-align:center;
            border:1px solid #E7F5E8;
            box-shadow:0 8px 22px rgba(0,0,0,.08);
            ">

            <h3 style="color:#166534;">
            🥗 Nutri Score
            </h3>

            <div style="
            width:130px;
            height:130px;
            margin:auto;
            border-radius:50%;
            background:{colors.get(grade)};
            display:flex;
            justify-content:center;
            align-items:center;
            font-size:48px;
            font-weight:900;
            color:white;
            margin-top:20px;
            margin-bottom:20px;
            ">

            {grade}

            </div>

            <h4 style="color:#555;">
            Food Quality Rating
            </h4>

            </div>
            """, unsafe_allow_html=True)

        
        st.divider()

        st.markdown("""
        <h2 style="
        color:#14532D;
        font-weight:800;
        margin-top:20px;
        margin-bottom:15px;
        ">
        💡 Healthier Alternatives
        </h2>
        """, unsafe_allow_html=True)

# Known foods → Local alternatives
        if not gemini_used:

            alternatives = ALTERNATIVES.get(food, [])

# Unknown foods → AI alternatives
        else:

            alternatives = get_alternatives(food)

        if alternatives:

            for alt in alternatives:
                st.markdown(f"""
                <div style="
                background:#F4FFF4;
                padding:15px;
                border-radius:15px;
                border-left:6px solid #43A047;
                margin-bottom:10px;
                color:#14532D;
                font-weight:600;
                ">
                ✅ {alt.replace("_"," ").title()}
                </div>
                """, unsafe_allow_html=True)

        else:

            st.info("No healthier alternatives available.")


        st.divider()
        st.divider()

        st.markdown("""
        <h2 style="
        color:#14532D;
        font-weight:800;
        margin-top:20px;
        margin-bottom:15px;
        ">
        🚦 Meal Risk Analysis
        </h2>
        """, unsafe_allow_html=True)

        risk, reasons = meal_risk(info)

        if risk == "LOW":
            st.success("🟢 LOW RISK")

        elif risk == "MEDIUM":
            st.warning("🟡 MEDIUM RISK")

        else:
            st.error("🔴 HIGH RISK")

        for reason in reasons:
            st.write("✔", reason)

        st.markdown("""
        <h2 style="
        color:#14532D;
        font-weight:800;
        margin-top:20px;
        margin-bottom:15px;
        ">
        🤖 AI Nutrition Coach
        </h2>
        """, unsafe_allow_html=True)

        advice = get_ai_advice(food, info)

        for item in advice:

            st.markdown(f"""
            <div style="
            background:#F7FFF7;
            border-left:6px solid #2E7D32;
            padding:15px;
            margin-bottom:12px;
            border-radius:15px;
            color:#1B4332;
            font-size:16px;
            box-shadow:0 4px 12px rgba(0,0,0,.05);
            ">
            {item}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <h2 style="
        color:#14532D;
        font-weight:800;
        margin-top:20px;
        margin-bottom:15px;
        ">
        🍽 Save This Meal
        </h2>
        """, unsafe_allow_html=True)

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
                st.success(f"🤖 AI identified: {food}")
                st.info(result.get("advice", "No AI advice available."))
            save_meal(
                uid,
                food,
                info,
                meal_type
            )

            st.success("✅ Meal Saved Successfully!")
            st.balloons()

