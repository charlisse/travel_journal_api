from flask import Blueprint, request, jsonify
from extensions import db
from models import Entry, Trip
from utils import error_response, validate_fields, parse_date

bp = Blueprint("entries", __name__, url_prefix="/entries")


# -------------------- Entry CRUD --------------------

@bp.route("/", methods=["GET"])
def list_entries():
    entries = Entry.query.all()
    return jsonify([e.to_dict() for e in entries]), 200


@bp.route("/", methods=["POST"])
def create_entry():
    data = request.get_json() or {}
    valid, msg = validate_fields(data, ["trip_id", "date", "title", "content"])
    if not valid:
        return error_response(msg, 400)

    trip = Trip.query.get(data["trip_id"])
    if not trip:
        return error_response("Trip not found", 404)

    try:
        entry_date = parse_date(data["date"], "date")
    except ValueError as ve:
        return error_response(str(ve), 400)

    entry = Entry(
        trip_id=trip.id,
        date=entry_date,
        title=data["title"],
        content=data["content"]
    )
    db.session.add(entry)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "Entry created", "entry": entry.to_dict()}), 201


@bp.route("/<int:entry_id>", methods=["GET"])
def get_entry(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        return error_response("Entry not found", 404)
    return jsonify(entry.to_dict()), 200


@bp.route("/<int:entry_id>", methods=["PUT"])
def update_entry(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        return error_response("Entry not found", 404)

    data = request.get_json() or {}

    if "title" in data and data["title"]:
        entry.title = data["title"]
    if "content" in data and data["content"]:
        entry.content = data["content"]
    if "date" in data and data["date"]:
        try:
            entry.date = parse_date(data["date"], "date")
        except ValueError as ve:
            return error_response(str(ve), 400)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "Entry updated", "entry": entry.to_dict()}), 200


@bp.route("/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        return error_response("Entry not found", 404)

    db.session.delete(entry)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "Entry deleted"}), 200
