from flask import Blueprint, request, jsonify
from extensions import db
from models import Trip, User, UserTrip
from utils import error_response, validate_fields, parse_date

bp = Blueprint("trips", __name__, url_prefix="/trips")


# ----------------------------
# CRUD for trips
# ----------------------------
@bp.route("/", methods=["GET"])
def list_trips():
    trips = Trip.query.all()
    return jsonify([t.to_dict() for t in trips]), 200


@bp.route("/", methods=["POST"])
def create_trip():
    data = request.get_json() or {}
    valid, msg = validate_fields(data, ["title", "start_date", "end_date", "location"])
    if not valid:
        return error_response(msg, 400)

    try:
        start = parse_date(data["start_date"], "start_date")
        end = parse_date(data["end_date"], "end_date")
    except ValueError as ve:
        return error_response(str(ve), 400)

    if end < start:
        return error_response("end_date cannot be earlier than start_date", 400)

    trip = Trip(
        title=data["title"],
        start_date=start,
        end_date=end,
        location=data["location"]
    )
    db.session.add(trip)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "Trip created", "trip": trip.to_dict()}), 201


@bp.route("/<int:trip_id>", methods=["GET"])
def get_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return error_response("Trip not found", 404)
    return jsonify(trip.to_dict()), 200


@bp.route("/<int:trip_id>", methods=["PUT"])
def update_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return error_response("Trip not found", 404)

    data = request.get_json() or {}
    if "title" in data and data["title"]:
        trip.title = data["title"]
    if "location" in data and data["location"]:
        trip.location = data["location"]
    if "start_date" in data and data["start_date"]:
        try:
            trip.start_date = parse_date(data["start_date"], "start_date")
        except ValueError as ve:
            return error_response(str(ve), 400)
    if "end_date" in data and data["end_date"]:
        try:
            trip.end_date = parse_date(data["end_date"], "end_date")
        except ValueError as ve:
            return error_response(str(ve), 400)

    if trip.end_date < trip.start_date:
        return error_response("end_date cannot be earlier than start_date", 400)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "Trip updated", "trip": trip.to_dict()}), 200


@bp.route("/<int:trip_id>", methods=["DELETE"])
def delete_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return error_response("Trip not found", 404)

    # Delete associated UserTrip links automatically
    UserTrip.query.filter_by(trip_id=trip.id).delete()

    db.session.delete(trip)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "Trip deleted"}), 200


# ----------------------------
# Manage users on a trip
# ----------------------------
@bp.route("/<int:trip_id>/users", methods=["GET"])
def list_trip_users(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return error_response("Trip not found", 404)

    links = UserTrip.query.filter_by(trip_id=trip.id).all()
    user_ids = [l.user_id for l in links]
    users = User.query.filter(User.id.in_(user_ids)).all()
    return jsonify([u.to_dict() for u in users]), 200


@bp.route("/<int:trip_id>/users", methods=["POST"])
def add_user_to_trip(trip_id):
    data = request.get_json() or {}
    valid, msg = validate_fields(data, ["user_id"])
    if not valid:
        return error_response(msg, 400)

    trip = Trip.query.get(trip_id)
    if not trip:
        return error_response("Trip not found", 404)

    user = User.query.get(data["user_id"])
    if not user:
        return error_response("User not found", 404)

    exists = UserTrip.query.filter_by(user_id=user.id, trip_id=trip.id).first()
    if exists:
        return error_response("User already linked to this trip", 400)

    link = UserTrip(user_id=user.id, trip_id=trip.id)
    db.session.add(link)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({
        "message": "User added to trip",
        "link": link.to_dict()
    }), 201


@bp.route("/<int:trip_id>/users/<int:user_id>", methods=["DELETE"])
def remove_user_from_trip(trip_id, user_id):
    link = UserTrip.query.filter_by(trip_id=trip_id, user_id=user_id).first()
    if not link:
        return error_response("Link not found", 404)

    db.session.delete(link)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return error_response(f"Database error: {e}", 500)

    return jsonify({"message": "User removed from trip"}), 200
