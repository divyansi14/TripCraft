import os
import pandas as pd
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from planner.budget_optimizer import apply_budget
from planner.scheduler import schedule
from backend.poi_fetcher import fetch_pois
from backend.itinerary_engine import build_itinerary
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "places.csv")
ML_PATH = os.path.join(BASE_DIR, "ml")

# Load datasets
places_df = pd.read_csv(DATA_PATH)

# Load ML models
popularity_model = joblib.load(os.path.join(ML_PATH, "popularity_model.pkl"))
recommender_model = joblib.load(os.path.join(ML_PATH, "recommender_model.pkl"))
interest_encoder = joblib.load(os.path.join(ML_PATH, "interest_encoder.pkl"))
category_encoder = joblib.load(os.path.join(ML_PATH, "category_encoder.pkl"))




app = FastAPI(title="TripCraft AI")

@app.get("/generate-itinerary")
def generate_itinerary(city: str, budget: int, days: int):
    itinerary = build_itinerary(city, budget, days)
    return {
        "city": city,
        "budget": budget,
        "days": days,
        "itinerary": itinerary
    }



@app.post("/generate-trip")
def generate_trip(user_input: dict):
    days = user_input["days"]
    budget = user_input["budget"]
    interest = user_input["interest"]

    # ---- Popularity Prediction ----
    features = places_df[["rating", "avg_time_spent", "cost"]]
    places_df["predicted_popularity"] = popularity_model.predict(features)

    # ---- Interest-based Recommendation ----
    interest_enc = interest_encoder.transform([interest])[0]

    def interest_score(category):
        try:
            cat_enc = category_encoder.transform([category])[0]
            return recommender_model.predict_proba([[interest_enc, cat_enc]])[0][1]
        except:
            return 0.0

    places_df["interest_score"] = places_df["category"].apply(interest_score)

    # ---- Final Ranking (ML Fusion) ----
    places_df["final_score"] = (
        0.6 * places_df["predicted_popularity"] +
        0.4 * places_df["interest_score"]
    )

    ranked_places = places_df.sort_values(
        by="final_score", ascending=False
    ).to_dict(orient="records")

    # ---- Budget Optimization ----
    filtered = apply_budget(ranked_places, budget)

    # ---- Scheduling ----
    plan = schedule(filtered, days)

    return plan