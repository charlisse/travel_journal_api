from datetime import date
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


# ----------------------------
# Users
# ----------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    trips = db.relationship("UserTrip", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


# ----------------------------
# Trips
# ----------------------------
class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(120), nullable=False)

    users = db.relationship("UserTrip", back_populates="trip", cascade="all, delete-orphan")
    entries = db.relationship("Entry", back_populates="trip", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "location": self.location,
        }


# ----------------------------
# UserTrips (association)
# ----------------------------
class UserTrip(db.Model):
    __tablename__ = "user_trips"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)

    user = db.relationship("User", back_populates="trips")
    trip = db.relationship("Trip", back_populates="users")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "trip_id": self.trip_id,
        }


# ----------------------------
# Entries
# ----------------------------
class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)

    trip = db.relationship("Trip", back_populates="entries")
    photos = db.relationship("Photo", back_populates="entry", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "date": self.date.isoformat(),
            "title": self.title,
            "content": self.content,
        }


# ----------------------------
# Photos
# ----------------------------
class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.id"), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))

    entry = db.relationship("Entry", back_populates="photos")

    def to_dict(self):
        return {
            "id": self.id,
            "entry_id": self.entry_id,
            "url": self.url,
            "caption": self.caption,
        }
