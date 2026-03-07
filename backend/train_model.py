import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "places.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def main():
    df = pd.read_csv(DATA_PATH)

    required_columns = {"rating", "popularity", "cost"}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in dataset: {sorted(missing)}")

    # Create a learnable target if score is not present.
    if "score" not in df.columns:
        df["score"] = (df["rating"] * 2.0) + (df["popularity"] * 5.0) - (df["cost"] * 0.001)

    X = df[["rating", "popularity", "cost"]]
    y = df["score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    joblib.dump(model, MODEL_PATH)

    print(f"Model trained. MSE: {mse:.6f}")
    print(f"Model saved: {MODEL_PATH}")


if __name__ == "__main__":
    main()
