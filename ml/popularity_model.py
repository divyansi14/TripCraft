# ml/popularity_model.py
import os
import pandas as pd
import joblib
import numpy as np
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "places.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)

X = df[['rating', 'avg_time_spent', 'cost']]
y = df['popularity']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "popularity_model.pkl")
joblib.dump(model, MODEL_PATH)

print("✅ Popularity model trained & saved at:", MODEL_PATH)


# After prediction
y_pred = model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Create prediction matrix
prediction_matrix = np.column_stack([
    np.arange(1, len(y_test) + 1),
    y_test.values,
    y_pred,
    np.abs(y_test.values - y_pred)
])

print("\n" + "="*70)
print("📈 POPULARITY MODEL EVALUATION")
print("="*70)
print(f"✅ Model trained & saved at: {MODEL_PATH}")
print(f"\n📊 Performance Metrics:")
print(f"   • R² Score: {r2:.4f}")
print(f"   • Mean Absolute Error (MAE): {mae:.4f}")
print(f"   • Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"   • Mean Squared Error (MSE): {mse:.4f}")

print(f"\n📋 Prediction Matrix (Sample size: {len(y_test)}):")
print(f"   {'Index':<8} {'Actual':<12} {'Predicted':<12} {'Error':<12}")
print("-" * 50)
for i, row in enumerate(prediction_matrix[:10]):  # Show first 10 predictions
    idx, actual, pred, error = row
    print(f"   {int(idx):<8} {actual:<12.4f} {pred:<12.4f} {error:<12.4f}")
if len(prediction_matrix) > 10:
    print(f"   ... ({len(prediction_matrix) - 10} more rows)")

print("\n📊 Full Prediction Matrix:")
print(prediction_matrix)
print("="*70)

# Save metrics to JSON for frontend visualization
metrics = {
    "r2_score": round(r2, 4),
    "mae": round(mae, 4),
    "rmse": round(rmse, 4),
    "mse": round(mse, 4),
    "predictions": prediction_matrix.tolist()
}

with open(os.path.join(BASE_DIR, "backend", "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=2)

print("📊 Metrics saved for frontend visualization at: backend/metrics.json")