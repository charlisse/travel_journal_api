import os
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()

# Base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Use DATABASE_URL if set (Render/Postgres), otherwise fallback to local SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(basedir, 'instance', 'travel_journal.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallbacksecret")

    # Optional: set debug mode from env
    DEBUG = os.environ.get("FLASK_ENV") != "production"
