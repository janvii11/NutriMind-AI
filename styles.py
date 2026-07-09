import streamlit as st

def load_css():
    st.markdown("""
    <style>

    .stApp{
        background:#0F172A;
        color:#F8FAFC;
    }

    section[data-testid="stSidebar"]{
        background:#111827;
    }

    h1,h2,h3,h4,h5,h6{
        color:white;
        font-weight:700;
    }

    div[data-testid="stMetric"]{
        background:#1E293B;
        padding:18px;
        border-radius:15px;
        border:1px solid #334155;
    }

    .stButton>button{
        background:#2563EB;
        color:white;
        border:none;
        border-radius:12px;
        padding:12px;
        font-weight:600;
    }

    .stButton>button:hover{
        background:#1D4ED8;
    }

    .stFileUploader{
        border:2px dashed #3B82F6;
        border-radius:15px;
        padding:15px;
    }

    hr{
        border-color:#334155;
    }

    </style>
    """, unsafe_allow_html=True)