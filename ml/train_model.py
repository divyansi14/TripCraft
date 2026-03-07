# ml/train_model.py
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

places = pd.read_csv("data/places.csv")
interactions = pd.read_csv("data/user_interactions.csv")

category_encoder = joblib.load("ml/category_encoder.pkl")
interest_encoder = joblib.load("ml/interest_encoder.pkl")

rows = []

for _, inter in interactions.iterrows():
    place = places[places["place_id"] == inter["place_id"]].iloc[0]

    distance = np.random.uniform(1, 20)  # simulated travel distance

    rows.append([
        place["rating"],
        place["popularity"],
        place["avg_cost"],
        distance,
        category_encoder.transform([place["category"]])[0],
        interest_encoder.transform([inter["interest_type"]])[0],
        inter["visited"]   # LABEL
    ])

dataset = pd.DataFrame(rows, columns=[
    "rating",
    "popularity",
    "avg_cost",
    "distance",
    "category_enc",
    "interest_enc",
    "label"
])

dataset.to_csv("data/dataset.csv", index=False)
print("✅ ML dataset created successfully")


X = dataset.drop("label", axis=1)
y = dataset["label"]

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5)

model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

print("Validation Performance:")
print(classification_report(y_val, model.predict(X_val)))

print("Test Performance:")
print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, "ml/recommender_model.pkl")