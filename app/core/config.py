import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, '../../data/coding.db')}"
    )

    MODEL_PATH = os.getenv("MODEL_PATH", "saved_models/model.pkl")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")