import pandas as pd
import os
import sys
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from poi_fetcher import fetch_pois

# --------------------------------------------------
# FASTAPI APP INITIALIZATION
# --------------------------------------------------
app = FastAPI(title="TripCraft – Real-Time Itinerary Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("[OK] Backend initialized - Using real-time data from OpenStreetMap")

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Real-time Itinerary Generator Backend",
        "status": "ok"
    }


@app.post("/plan")
async def generate_itinerary(request: Request):
    try:
        data = await request.json()

        city = data.get("city", "").strip()
        budget = int(data.get("budget", 0))
        days = int(data.get("days", 1))

        print(f"\n[REQUEST] City={city}, Budget=₹{budget}, Days={days}")

        if not city:
            raise HTTPException(status_code=400, detail="City name is required")

        if budget <= 0 or days <= 0:
            raise HTTPException(status_code=400, detail="Budget and days must be positive")

        # --------------------------------------------------
        # FETCH REAL-TIME POIs
        # --------------------------------------------------
        print(f"[FETCHING] Real-time places from {city}...")
        places = fetch_pois(city)

        if not places:
            raise HTTPException(
                status_code=404,
                detail=f"No places found for {city}. Try another city."
            )

        df = pd.DataFrame(places)

        # Filter by budget
        filtered = df[df["cost"] <= budget].sort_values(
            by="popularity", ascending=False
        )

        if filtered.empty:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": f"No affordable places in {city} within ₹{budget}",
                    "min_budget": int(df["cost"].min())
                }
            )

        # --------------------------------------------------
        # DAY-WISE ITINERARY
        # --------------------------------------------------
        itinerary = {}
        places_per_day = max(1, len(filtered) // days)

        index = 0
        for day in range(1, days + 1):
            end_index = index + places_per_day
            if day == days:
                end_index = len(filtered)

            day_places = filtered.iloc[index:end_index]
            day_data = []

            for _, place in day_places.iterrows():
                day_data.append({
                    "name": place["name"],
                    "category": place["category"],
                    "cost": int(place["cost"]),
                    "rating": round(place["rating"], 1),
                    "popularity": int(place["popularity"]),
                    "city": place["city"]
                })

            if day_data:
                itinerary[f"Day {day}"] = day_data

            index = end_index

        print(f"[OK] Itinerary generated for {city}")
        return itinerary

    except HTTPException as e:
        raise e
    except Exception as e:
        print("[ERROR]", str(e))
        raise HTTPException(status_code=500, detail=str(e))
