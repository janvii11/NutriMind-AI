import json
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = BASE_DIR / "data" / "user_profile.json"

def save_profile(profile):
    with open(FILE_NAME, "w") as f:
        json.dump(profile, f, indent=4)

def load_profile():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return None