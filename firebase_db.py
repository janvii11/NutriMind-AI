import pandas as pd
from firebase_config import db
from datetime import datetime
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

# ---------------- Save Meal ----------------

def save_meal(uid, food, info, meal_type):
    print("UID =", uid)
    print("FOOD =", food)
    print("INFO =", info)
    print("MEAL =", meal_type)
    meal = {
        "Food": food,
        "Meal_Type": meal_type,
        "Calories": info["Calories"],
        "Protein": info["Protein"],
        "Carbs": info["Carbs"],
        "Fat": info["Fat"],
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Timestamp": SERVER_TIMESTAMP
    }
    print(meal)
    db.collection("users") \
      .document(uid) \
      .collection("meals") \
      .add(meal)
    print("Meal uploaded successfully")

# ---------------- Load Meals ----------------

def load_meals(uid):

    docs = (
        db.collection("users")
        .document(uid)
        .collection("meals")
        .stream()
    )

    meals = []

    for doc in docs:

        meals.append(doc.to_dict())

    return meals


# ---------------- Delete Meals ----------------

def delete_meals(uid):

    docs = (
        db.collection("users")
        .document(uid)
        .collection("meals")
        .stream()
    )

    for doc in docs:

        doc.reference.delete()

def get_meals_dataframe(uid):

    docs = (
        db.collection("users")
        .document(uid)
        .collection("meals")
        .stream()
    )

    meals = []

    for doc in docs:
        meals.append(doc.to_dict())

    if len(meals) == 0:
        return pd.DataFrame()

    return pd.DataFrame(meals)
def save_profile(uid, profile):
    db.collection("users").document(uid).set(profile)


def load_profile(uid):
    doc = db.collection("users").document(uid).get()

    if doc.exists:
        return doc.to_dict()

    return None 