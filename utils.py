from flask import jsonify
from datetime import datetime, date


def error_response(message, status_code=400):
    return jsonify({"error": message}), status_code


def validate_fields(data, required_fields):
    missing = [f for f in required_fields if f not in data or data[f] in (None, "", [])]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None


def parse_date(value: str, field_name: str):
    """
    Parse ISO date (YYYY-MM-DD). Raise ValueError with a helpful message.
    """
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        raise ValueError(f"Field '{field_name}' must be an ISO date string 'YYYY-MM-DD'.")
