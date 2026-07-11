import streamlit as st

def is_logged_in():
    return st.session_state.get("logged_in", False)

def get_uid():
    return st.session_state.get("uid", None)

def get_email():
    return st.session_state.get("email", None)

def logout():
    st.session_state.clear()