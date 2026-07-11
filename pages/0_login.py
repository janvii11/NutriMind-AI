import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
from firebase_auth import login, signup
from styles import load_css
load_css()
st.markdown("""
<style>
.main-box{
    max-width:550px;
    margin:auto;
    margin-top:20px;
    padding:35px;
    border-radius:20px;
    background:rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    box-shadow:0px 10px 30px rgba(0,0,0,0.25);
}
.title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#00E5FF;
}
.subtitle{
    text-align:center;
    color:#CFCFCF;
    font-size:17px;
}
</style>

<div class="main-box">

<div class="title">
🥗 NutriMind AI
</div>

<div class="subtitle">
AI Powered Food Recognition & Nutrition Intelligence
</div>

<br>

</div>
""", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Login", "Signup"])

with tab1:
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("🚀 Login", use_container_width=True):
        user = login(email, password)

        if user:
            st.session_state["logged_in"] = True
            st.session_state["uid"] = user["localId"]
            st.session_state["email"] = user["email"]
            with st.spinner("Logging in..."):
                st.success("✅ Welcome to NutriMind AI")
                st.balloons()
            st.rerun()
        else:
            st.error("Invalid Email or Password")
with tab2:
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Create Account", use_container_width=True):
        user = signup(email, password)

        if user:
            st.success("Account Created Successfully 🎉")
        else:
            st.error("Signup Failed")