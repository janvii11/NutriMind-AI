import requests

API_KEY = "AIzaSyDFzDBWha9FoXqdBU5UnwEiYWOwSvoSDLU"


def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    r = requests.post(url, json=data)

    if r.status_code == 200:
        return r.json()

    return None


def signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"

    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    r = requests.post(url, json=data)

    if r.status_code == 200:
        return r.json()

    return None