import streamlit as st
import firebase_admin

from firebase_admin import credentials, firestore


if not firebase_admin._apps:

    firebase_key = st.secrets["FIREBASE_KEY"]

    cred = credentials.Certificate(dict(firebase_key))

    firebase_admin.initialize_app(cred)


db = firestore.client()