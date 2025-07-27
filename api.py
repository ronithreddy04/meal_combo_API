import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import random

app = FastAPI()

# Load meal data
df = pd.read_csv("meal_items.csv")

# Separate categories
mains = df[df["Category"] == "Main"]
sides = df[df["Category"] == "Side"]
drinks = df[df["Category"] == "Drink"]

# Generate all combos
combos = []

for _, main in mains.iterrows():
    for _, side in sides.iterrows():
        for _, drink in drinks.iterrows():
            total_cal = main['Calories'] + side['Calories'] + drink['Calories']
            total_pop = main['Popularity'] + side['Popularity'] + drink['Popularity']
            combos.append({
                "Main": main["Item"],
                "Side": side["Item"],
                "Drink": drink["Item"],
                "Calories": total_cal,
                "Popularity": total_pop
            })

# Pick target calorie and popularity
target_cal = combos[0]["Calories"]
target_pop = combos[0]["Popularity"]

# Filter only matching combos
valid_combos = [c for c in combos if c["Calories"] == target_cal and c["Popularity"] == target_pop]

# Function to return random combo
def get_random_combo():
    combo = random.choice(valid_combos)
    explanation = (
        f"This combo contains {combo['Main']}, {combo['Side']}, and {combo['Drink']} "
        f"with a total of {combo['Calories']} calories and popularity score of {combo['Popularity']}."
    )
    return {
        "weekday": datetime.now().strftime("%A"),
        "combo": {
            "Main": combo["Main"],
            "Side": combo["Side"],
            "Drink": combo["Drink"]
        },
        "explanation": explanation
    }

# 👉 Make this return combo directly on homepage
@app.get("/")
def show_combo():
    return JSONResponse(content=get_random_combo())
@app.get("/combo")
def show_combo_again():
    return JSONResponse(content=get_random_combo())
