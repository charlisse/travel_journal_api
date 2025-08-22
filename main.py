import os
from flask import Flask, jsonify
from extensions import db

def create_app():
    app = Flask(__name__)

    # Database config (uses env var if present, else sqlite file)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///instance/travel_journal.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init DB
    db.init_app(app)

    # Import models so tables are registered
    from models import User, Trip, UserTrip, Entry, Photo  # noqa: F401

    # Import and register blueprints from routes/
    from routes.users_routes import bp as users_bp
    from routes.trips_routes import bp as trips_bp
    from routes.entries_routes import bp as entries_bp
    from routes.photos_routes import bp as photos_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(entries_bp)
    app.register_blueprint(photos_bp)

    @app.route("/")
    def index():
        return jsonify({"message": "Travel Journal API (Users • Trips • Entries • Photos)"}), 200

    # Create tables on first run (dev-friendly)
    with app.app_context():
        db.create_all()

    return app


# Create the app instance
app = create_app()

if __name__ == "__main__":
    # Debug mode ON for development; change port if needed
    app.run(debug=True, port=5000)
