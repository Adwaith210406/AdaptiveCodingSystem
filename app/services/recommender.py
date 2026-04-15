from app.db.database import load_user_data
from app.ml.features import create_features
from app.ml.model import DifficultyModel

model = None

def get_model():
    global model
    if model is None:
        model = DifficultyModel()
        model.load()
    return model


def predict_next_difficulty(user_id: int):
    df = load_user_data(user_id)

    # 🔥 STRICT NEW USER CHECK
    if df is None or df.empty:
        return "easy"

    features = create_features(df)

    if features.empty:
        return "easy"

    accuracy = features["accuracy"].values[0]
    attempts = features["attempts"].values[0]

    print("DEBUG → accuracy:", accuracy, "attempts:", attempts)

    # 🔥 FORCE BEGINNER STAGE
    if attempts <= 3:
        return "easy"

    # 🔥 CONTROLLED PROGRESSION
    if accuracy < 0.5:
        return "easy"
    elif accuracy < 0.75:
        return "medium"
    else:
        return "hard"