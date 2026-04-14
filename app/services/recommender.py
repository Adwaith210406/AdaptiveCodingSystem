import pandas as pd
from app.ml.model import DifficultyModel
from app.ml.features import create_features
from app.db.database import load_user_data

model = None

def get_model():
    global model
    if model is None:
        model = DifficultyModel()
        model.load()
    return model


def predict_next_difficulty(user_id: int):
    df = load_user_data(user_id)

    if df.empty:
        return "easy"

    features = create_features(df)

    if features.empty:
        return "easy"

    X = features[["accuracy", "attempts", "avg_time"]]

    model_instance = get_model()

    return model_instance.predict(X)[0]