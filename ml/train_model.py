import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
df = pd.read_csv("../data/places.csv")

# Create ML target score
df["score"] = df["rating"] * 2 + df["popularity"] * 5 - df["cost"] * 0.001

# Features
X = df[["rating", "popularity", "cost"]]

# Target
y = df["score"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100)

model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model.pkl")

print("Model trained and saved as model.pkl")