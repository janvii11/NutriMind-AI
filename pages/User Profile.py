import streamlit as st

if not st.session_state.get("logged_in"):
    st.warning("🔒 Please login first.")
    st.stop()
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from firebase_db import save_profile, load_profile
from session_manager import get_uid
from styles import load_css
load_css()

st.markdown("""
<div style="
background:linear-gradient(135deg,#F3FAF3,#E8F5E9,#DDF5D8);
padding:35px;
border-radius:25px;
box-shadow:0 10px 25px rgba(46,125,50,.10);
margin-bottom:25px;
">

<h1 style="
text-align:center;
color:#14532D;
font-size:42px;
font-weight:900;
">

👤 User Health Profile

</h1>

<p style="
text-align:center;
color:#355E3B;
font-size:18px;
">

Manage your health profile & personalize your nutrition journey.

</p>

</div>
""", unsafe_allow_html=True)

uid = st.session_state.get("uid")
if uid:
    profile = load_profile(uid)
else:
    profile = None
if profile is None:
    profile = {}

# ---------------- Personal Information ----------------
st.markdown("""
<div style="
background:white;
padding:30px;
border-radius:20px;
border:1px solid #E8F5E9;
box-shadow:0 8px 20px rgba(46,125,50,.08);
margin-bottom:20px;
">
<h3 style="color:#14532D;">
📝 Personal Information
</h3>
""", unsafe_allow_html=True)
name = st.text_input(
    "Name",
    value=profile.get("name", "") if profile else ""
)

age = st.number_input(
    "Age",
    1,
    100,
    value=profile.get("age", 20) if profile else 20
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female", "Other"]
)

height = st.number_input(
    "Height (cm)",
    50,
    250,
    value=profile.get("height", 170) if profile else 170
)

weight = st.number_input(
    "Weight (kg)",
    20,
    250,
    value=profile.get("weight", 60) if profile else 60
)

goal = st.selectbox(
    "Goal",
    [
        "Weight Loss",
        "Weight Gain",
        "Maintain Weight",
        "Muscle Gain"
    ]
)

activity = st.selectbox(
    "Activity Level",
    [
        "Sedentary",
        "Light",
        "Moderate",
        "Active"
    ]
)

disease = st.multiselect(
    "Disease",
    [
        "None",
        "Diabetes",
        "PCOS",
        "Hypertension",
        "Heart Disease",
        "Thyroid"
    ]
)

allergy = st.text_input("Allergies")

diet = st.selectbox(
    "Diet Preference",
    [
        "Vegetarian",
        "Eggetarian",
        "Vegan",
        "Non Vegetarian"
    ]
)
st.markdown("</div>", unsafe_allow_html=True)
st.divider()

if st.button("💾 Save Profile", use_container_width=True):

    # ---------------- BMI ----------------

    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 1)

    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 25:
        bmi_status = "Healthy"
    elif bmi < 30:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    # ---------------- BMR ----------------

    if gender == "Male":
        bmr = round(10 * weight + 6.25 * height - 5 * age + 5)

    elif gender == "Female":
        bmr = round(10 * weight + 6.25 * height - 5 * age - 161)

    else:
        bmr = round(10 * weight + 6.25 * height - 5 * age)

    # ---------------- TDEE ----------------

    activity_factor = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725
    }

    tdee = round(bmr * activity_factor[activity])

    # ---------------- Target Calories ----------------

    if goal == "Weight Loss":
        target_calories = tdee - 500

    elif goal == "Weight Gain":
        target_calories = tdee + 500

    elif goal == "Muscle Gain":
        target_calories = tdee + 300

    else:
        target_calories = tdee

    # ---------------- Save Profile ----------------

    profile = {
        "name": name,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "goal": goal,
        "activity": activity,
        "disease": disease,
        "allergy": allergy,
        "diet": diet,
        "bmi": bmi,
        "bmi_status": bmi_status,
        "bmr": bmr,
        "tdee": tdee,
        "target_calories": target_calories
    }

    uid = st.session_state.get("uid")

    if uid:
        save_profile(uid, profile)
        st.success("✅ Profile saved to Firebase")
    else:
        st.error("Please login first.")

    st.success("✅ Profile Saved Successfully!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🧮 BMI", bmi)

    with col2:
        st.metric("🔥 BMR", f"{bmr} kcal/day")

    with col3:
        st.metric("🎯 Daily Calories", f"{target_calories} kcal")

    if bmi_status == "Healthy":
        st.success(f"✅ BMI Status: {bmi_status}")
    elif bmi_status == "Underweight":
        st.warning(f"⚠️ BMI Status: {bmi_status}")
    else:
        st.error(f"⚠️ BMI Status: {bmi_status}")