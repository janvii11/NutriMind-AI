import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\Janvi\Desktop\nmai\meal_history.csv")

# Total calories eaten each day
daily_calories = df.groupby("Date")["Calories"].sum()

plt.figure(figsize=(8,5))
daily_calories.plot(kind="bar")

plt.title("Daily Calorie Intake")
plt.xlabel("Date")
plt.ylabel("Calories")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()