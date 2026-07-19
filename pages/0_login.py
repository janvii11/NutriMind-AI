import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st

from firebase_auth import login, signup
from styles import load_css

load_css()

st.set_page_config(
    page_title="NutriMind AI",
    page_icon="🥗",
    layout="centered"
)

st.markdown("""
<style>
body{
background:#FCFDFC;
}

.stApp{
background:linear-gradient(
180deg,
#FCFDFC,
#F6FBF7,
#FFFFFF
);
}

/* hide streamlit header */

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

/* card */

.login-card{

max-width:650px;

margin:60px auto 30px auto;

padding:50px;

background:white;

border-radius:32px;

border:1px solid #E5F3E8;

box-shadow:0 18px 45px rgba(34,139,34,.12);

}

/* logo */

.logo{

font-size:72px;

text-align:center;

margin-bottom:15px;

animation:float 3s ease infinite;

}

/* title */

.title{

font-size:48px;

font-weight:900;

text-align:center;

color:#166534;

letter-spacing:.5px;

margin-bottom:12px;

}

/* subtitle */

.subtitle{

text-align:center;

color:#6B7280;

font-size:17px;

max-width:470px;

margin:auto;

line-height:1.7;

margin-bottom:30px;

}
/* divider */

.line{

height:3px;

width:85%;

margin:25px auto;

border-radius:20px;

background:linear-gradient(90deg,#E8F5E9,#43A047,#E8F5E9);

}

/* tabs */

.stTabs [data-baseweb="tab"]{

height:52px;

background:#F5FBF5;

border-radius:14px;

font-size:17px;

font-weight:700;

padding:0 22px;

color:#2E7D32;

transition:.25s;

}

.stTabs [aria-selected="true"]{

background:linear-gradient(135deg,#43A047,#2E7D32)!important;

color:white!important;

box-shadow:0 8px 18px rgba(46,125,50,.25);

}

/* buttons */

.stButton>button{

height:56px;

border-radius:16px;

background:linear-gradient(135deg,#43A047,#2E7D32);

font-size:18px;

font-weight:700;

color:white;

border:none;

transition:.3s;

}

.stButton>button:hover{

transform:translateY(-3px);

background:linear-gradient(135deg,#2E7D32,#1B5E20);

}

/* text inputs */

.stTextInput input{

height:52px;

background:white;

border:2px solid #D7F3D9;

border-radius:14px;

font-size:16px;

padding-left:15px;

}

.stTextInput input:focus{

border:2px solid #43A047;

box-shadow:0 0 0 4px rgba(76,175,80,.12);

}
label{
color:#14532D !important;
font-weight:600 !important;
}

.stCheckbox label{
color:#355E3B !important;
}

h1,h2,h3{
color:#14532D;
}

.stMarkdown{
color:#355E3B;
}

.stTabs{
margin-top:20px;
}
@keyframes float{

0%{transform:translateY(0px);}

50%{transform:translateY(-8px);}

100%{transform:translateY(0px);}

}
</style>
""", unsafe_allow_html=True)

st.markdown("""

<div class="login-card">

<div class="logo">
🥗
</div>

<div class="title">
NutriMind AI
</div>

<div class="subtitle">

Smart Food Recognition &
Nutrition Intelligence Platform

</div>

<div class="line"></div>
            

</div>

""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔑 Login", "📝 Create Account"])
with tab1:

    st.markdown("""
    <h2 style="
    color:#14532D;
    font-size:34px;
    font-weight:800;
    margin-top:10px;
    margin-bottom:20px;
    ">
    👋 Welcome Back
    </h2>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "📧 Email Address",
        key="login_email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "🔒 Password",
        type="password",
        key="login_password",
        placeholder="Enter your password"
    )

    remember = st.checkbox("Remember Me")

    if st.button("🚀 Login", use_container_width=True):

        if email == "" or password == "":
            st.warning("Please fill all fields.")

        else:

            user = login(email, password)

            if user:

                st.session_state["logged_in"] = True
                st.session_state["uid"] = user["localId"]
                st.session_state["email"] = user["email"]

                with st.spinner("Signing you in..."):
                    st.success("Welcome Back 🌿")
                    st.balloons()

                st.rerun()

            else:

                st.error("Invalid Email or Password")


# ===================================================
# SIGNUP
# ===================================================

with tab2:

    st.markdown("""
    <h2 style="
    color:#14532D;
    font-size:34px;
    font-weight:800;
    margin-top:10px;
    margin-bottom:20px;
    ">
    🌱 Create Your Account
    </h2>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "📧 Email Address",
        key="signup_email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "🔒 Password",
        type="password",
        key="signup_password",
        placeholder="Minimum 6 characters"
    )

    confirm = st.text_input(
        "✅ Confirm Password",
        type="password",
        key="signup_confirm"
    )

    agree = st.checkbox(
        "I agree to the Terms & Privacy Policy"
    )

    if st.button(
        "🌱 Create Account",
        use_container_width=True
    ):

        if email == "" or password == "" or confirm == "":
            st.warning("Please fill all fields.")

        elif password != confirm:
            st.error("Passwords do not match.")

        elif len(password) < 6:
            st.error("Password must contain at least 6 characters.")

        elif not agree:
            st.warning("Please accept Terms & Privacy Policy.")

        else:

            user = signup(email, password)

            if user:

                st.success("🎉 Account Created Successfully!")

                st.info("You can now login using your credentials.")

            else:

                st.error("Signup Failed. Email may already exist.")