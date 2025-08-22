# Travel Journal API (Flask + SQLAlchemy)

Entities (ERD):
- Users (user_id, username, email, password_hash)
- Trips (trip_id, title, start_date, end_date, location)
- UserTrips (usertrip_id, user_id, trip_id)  ← many-to-many Users ↔ Trips
- Entries (entry_id, trip_id, date, title, content)
- Photos (photo_id, entry_id, url, caption)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate      
pip install -r requirements.txt
python main.py
