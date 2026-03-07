def preference_score(poi, preferences):
    return preferences.get(poi["category"], 0) / 100