from flask import Flask, jsonify
from extensions import db, migrate
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from models import User, Trip, UserTrip, Entry, Photo 

    # Register blueprints
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

    print("Using database:", app.config["SQLALCHEMY_DATABASE_URI"])

    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
