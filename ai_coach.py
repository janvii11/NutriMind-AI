from user_profile import load_profile


def get_ai_advice(food, info):

    profile = load_profile()

    advice = []

    calories = info["Calories"]
    protein = info["Protein"]
    fat = info["Fat"]
    carbs = info["Carbs"]
    health = info["Health_Score"]

    # ---------------- General ----------------

    if calories > 450:
        advice.append("🔥 This meal is high in calories. Keep your next meal lighter.")

    if protein < 12:
        advice.append("💪 Increase your protein intake by adding paneer, eggs, tofu or sprouts.")

    if fat > 20:
        advice.append("🥑 This meal contains high fat. Avoid another fried meal today.")

    if carbs > 60:
        advice.append("🍚 High carbohydrate meal detected. Balance it with vegetables and protein.")

    if health < 50:
        advice.append("🥗 This food has a low health score. Choose healthier alternatives more often.")

    # ---------------- Goal Based ----------------

    if profile:

        goal = profile.get("goal", "")

        if goal == "Weight Loss":
            advice.append("🎯 Your goal is Weight Loss. Stay within your daily calorie target.")

        elif goal == "Muscle Gain":
            advice.append("🏋️ Add a protein-rich snack after this meal.")

        elif goal == "Weight Gain":
            advice.append("🥜 Include healthy calorie-dense foods like nuts and peanut butter.")

        # ---------------- Disease Based ----------------

        diseases = profile.get("disease", [])

        if "PCOS" in diseases:
            advice.append("🌸 PCOS: Prefer low-GI foods and reduce sugary snacks.")

        if "Diabetes" in diseases:
            advice.append("🩸 Diabetes: Monitor carbohydrate intake and avoid sugary drinks.")

        if "Heart Disease" in diseases:
            advice.append("❤️ Reduce saturated fat and excess salt.")

        if "Hypertension" in diseases:
            advice.append("🧂 Limit sodium-rich processed foods.")

        if "Thyroid" in diseases:
            advice.append("🦋 Maintain a balanced iodine-rich diet as advised by your healthcare professional.")

    # ---------------- Universal ----------------

    advice.append("💧 Drink 2 glasses of water after your meal.")

    advice.append("🚶 Walk for 15–20 minutes after eating.")

    return advice