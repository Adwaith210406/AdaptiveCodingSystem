from flask import Blueprint, jsonify
from app.db.database import get_leaderboard, get_user_stats

leaderboard_bp = Blueprint("leaderboard", __name__)

@leaderboard_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    return jsonify(get_leaderboard())


@leaderboard_bp.route("/stats/<int:user_id>", methods=["GET"])
def stats(user_id):
    return jsonify(get_user_stats(user_id))
