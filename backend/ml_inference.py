import joblib
import numpy as np

model = joblib.load("ml/recommender_model.pkl")

def score_poi(poi, interest_enc=0):
    features = np.array([[
        poi["rating"],
        poi["popularity"],
        poi["avg_cost"],
        poi["distance"],
        0,                # category_enc (optional)
        interest_enc
    ]])
    return model.predict_proba(features)[0][1]