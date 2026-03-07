from backend.poi_fetcher import fetch_pois
from backend.ml_inference import score_poi
from backend.travel_utils import haversine, estimate_travel_cost
from backend.preference_engine import preference_score
from backend.weather_adjustment import weather_penalty
from backend.weather import get_weather

def build_itinerary(city, budget, days):
    pois = fetch_pois(city)
    daily_budget = budget / days

    # Compute distances from city center
    base_lat, base_lng = pois[0]["lat"], pois[0]["lng"]

    for poi in pois:
        poi["distance"] = haversine(
            base_lat, base_lng, poi["lat"], poi["lng"]
        )
        poi["travel_cost"] = estimate_travel_cost(poi["distance"])
        poi["score"] = score_poi(poi)

    pois.sort(key=lambda x: x["score"], reverse=True)

    itinerary = {}
    day = 1
    spent = 0
    itinerary[day] = []

    for poi in pois:
        total_cost = poi["avg_cost"] + poi["travel_cost"]

        if spent + total_cost <= daily_budget:
            itinerary[day].append({
                "place": poi["name"],
                "visit_cost": poi["avg_cost"],
                "travel_cost": poi["travel_cost"],
                "rating": poi["rating"]
            })
            spent += total_cost
        else:
            day += 1
            if day > days:
                break
            itinerary[day] = []
            spent = 0

    return itinerary



def compute_final_score(poi, preferences, weather):
    ml_score = poi["ml_score"]
    pref_score = preference_score(poi, preferences)
    weather_factor = weather_penalty(poi, weather)

    return (0.6 * ml_score + 0.4 * pref_score) * weather_factor

weather = get_weather(city)

for poi in pois:
    poi["ml_score"] = score_poi(poi)
    poi["final_score"] = compute_final_score(
        poi, preferences, weather
    )

pois.sort(key=lambda x: x["final_score"], reverse=True)