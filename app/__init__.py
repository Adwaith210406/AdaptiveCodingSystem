from flask import Flask
from flask_cors import CORS
from app.core.config import Config
from app.core.logger import setup_logger
from app.routes.recommend import recommend_bp
from app.routes.submit import submit_bp
from app.routes.analyze import analyze_bp
from app.routes.auth import auth_bp
from app.routes.leaderboard import leaderboard_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Setup logger
    logger = setup_logger(Config.LOG_LEVEL)
    logger.info("🚀 App starting...")

    # Register routes
    app.register_blueprint(recommend_bp)
    app.register_blueprint(submit_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(leaderboard_bp)

    return app