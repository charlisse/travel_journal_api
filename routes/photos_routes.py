from flask import Blueprint, request, jsonify
from extensions import db
from models import Photo, Entry
from utils import error_response, validate_fields

bp = Blueprint("photos", __name__, url_prefix="/photos")


# -------------------- Photo CRUD --------------------

@bp.route("/", methods=["GET"])
def list_photos():
    photos = Photo.query.all()
    return jsonify([p.to_dict() for p in photos]), 200


@bp.route("/", methods=["POST"])
def create_photo():
    data = request.get_json() or {}
    valid, msg = validate_fields(data, ["entry_id", "url"])
    if not valid:
        return error_response(msg, 400)

    entry = Entry.query.get(data["entry_id"])
    if not entry:
        return error_response("Entry not found", 404)

    photo = Photo(entry_id=entry.id, url=data["url"], caption=data.get("caption"))
    db.session.add(photo)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "Photo created", "photo": photo.to_dict()}), 201


@bp.route("/<int:photo_id>", methods=["GET"])
def get_photo(photo_id):
    photo = Photo.query.get(photo_id)
    if not photo:
        return error_response("Photo not found", 404)
    return jsonify(photo.to_dict()), 200


@bp.route("/<int:photo_id>", methods=["PUT"])
def update_photo(photo_id):
    photo = Photo.query.get(photo_id)
    if not photo:
        return error_response("Photo not found", 404)

    data = request.get_json() or {}
    if "url" in data and data["url"]:
        photo.url = data["url"]
    if "caption" in data:
        photo.caption = data["caption"]

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "Photo updated", "photo": photo.to_dict()}), 200


@bp.route("/<int:photo_id>", methods=["DELETE"])
def delete_photo(photo_id):
    photo = Photo.query.get(photo_id)
    if not photo:
        return error_response("Photo not found", 404)

    db.session.delete(photo)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "Photo deleted"}), 200
