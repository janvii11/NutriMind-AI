import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

if not firebase_admin._apps:

    try:
        

        st.write(type(st.secrets["FIREBASE_KEY"]))
        st.write(st.secrets["FIREBASE_KEY"].keys())
        st.stop()
        # Streamlit Cloud
        cred = credentials.Certificate(dict(st.secrets["FIREBASE_KEY"]))

    except Exception:
        # Local Laptop
        BASE_DIR = Path(__file__).resolve().parent
        KEY_PATH = BASE_DIR / "firebase_key.json"

        cred = credentials.Certificate(KEY_PATH)

    firebase_admin.initialize_app(cred)

db = firestore.client()