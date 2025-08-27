from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from utils import error_response, validate_fields

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    valid, msg = validate_fields(data, ["username", "email", "password"])
    if not valid:
        return error_response(msg, 400)

    if User.query.filter_by(username=data["username"]).first():
        return error_response("Username already exists", 400)
    if User.query.filter_by(email=data["email"]).first():
        return error_response("Email already exists", 400)

    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "User registered", "user": user.to_dict()}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    valid, msg = validate_fields(data, ["username", "password"])
    if not valid:
        return error_response(msg, 400)

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return error_response("Invalid username or password", 401)

    return jsonify({"message": f"Welcome, {user.username}!", "user": user.to_dict()}), 200

@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return error_response("User not found", 404)

    db.session.delete(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "User deleted"}), 200
