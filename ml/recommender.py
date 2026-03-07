import os
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

# Absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "user_interactions.csv")
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

# Load dataset
df = pd.read_csv(DATA_PATH)

# Encode categorical data
le_interest = LabelEncoder()
le_category = LabelEncoder()

df["interest_enc"] = le_interest.fit_transform(df["interest"])
df["category_enc"] = le_category.fit_transform(df["category"])

X = df[["interest_enc", "category_enc"]]
y = df["visited"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model & encoders
joblib.dump(model, os.path.join(MODEL_DIR, "recommender_model.pkl"))
joblib.dump(le_interest, os.path.join(MODEL_DIR, "interest_encoder.pkl"))
joblib.dump(le_category, os.path.join(MODEL_DIR, "category_encoder.pkl"))

print("✅ Recommender model & encoders saved successfully")