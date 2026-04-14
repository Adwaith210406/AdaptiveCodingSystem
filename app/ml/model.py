import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from app.core.config import Config


class DifficultyModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=200, max_depth=10)
        self.encoder = LabelEncoder()

    def load(self):
        data = joblib.load(Config.MODEL_PATH)
        self.model = data["model"]
        self.encoder = data["encoder"]

    def predict(self, features: pd.DataFrame):
        pred = self.model.predict(features)
        return self.encoder.inverse_transform(pred)