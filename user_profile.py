from firebase_config import db

# ---------------- SAVE PROFILE ----------------

def save_profile(uid, profile):

    db.collection("users") \
      .document(uid) \
      .set(profile, merge=True)


# ---------------- LOAD PROFILE ----------------

def load_profile(uid):

    doc = db.collection("users") \
            .document(uid) \
            .get()

    if doc.exists:
        return doc.to_dict()

    return {}