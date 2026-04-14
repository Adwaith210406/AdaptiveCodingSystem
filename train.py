import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

print("✅ Step 1: Imports started")

# Local imports (after print to debug hanging)
from app.db.database import load_data
print("✅ Step 2: Database module loaded")

from app.ml.features import create_features
print("✅ Step 3: Feature module loaded")


MODEL_PATH = "saved_models/model.pkl"


def train_model():
    print("🚀 Training model...")

    # -------------------------------
    # 📥 Load Data
    # -------------------------------
    df = load_data()
    print("✅ Data loaded:", len(df), "rows")

    if df.empty:
        raise ValueError("❌ Dataset is empty. Cannot train model.")

    # -------------------------------
    # 🧠 Feature Engineering
    # -------------------------------
    features = create_features(df)
    print("✅ Features created")

    # -------------------------------
    # 🎯 Get target labels
    # -------------------------------
    # Using latest difficulty per user
    latest = df.sort_values("problem_id").groupby("user_id").tail(1)

    dataset = features.merge(
        latest[["user_id", "difficulty"]],
        on="user_id"
    )

    print("✅ Dataset merged")

    X = dataset[["accuracy", "attempts", "avg_time"]]
    y = dataset["difficulty"]

    # -------------------------------
    # 🔤 Encode labels
    # -------------------------------
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    print("✅ Labels encoded")

    # -------------------------------
    # 🌲 Train Model
    # -------------------------------
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )

    model.fit(X, y_encoded)
    print("✅ Model trained")

    # -------------------------------
    # 💾 Save Model
    # -------------------------------
    joblib.dump({
        "model": model,
        "encoder": encoder
    }, MODEL_PATH)

    print("🎉 Model trained and saved at:", MODEL_PATH)


# -------------------------------
# ▶️ ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    try:
        train_model()
    except Exception as e:
        print("❌ Error during training:", str(e))