from flask import Flask
from app.core.config import Config
from app.core.logger import setup_logger
from app.routes.recommend import recommend_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup logger
    logger = setup_logger(Config.LOG_LEVEL)
    logger.info("🚀 App starting...")

    # Register routes
    app.register_blueprint(recommend_bp)

    return app