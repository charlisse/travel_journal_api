# Travel Journal API

An API for managing travel journals, built with Flask and PostgreSQL. Users can create accounts, log trips, and view trips from other users. 

## Features
- User registration and authentication  
- Create, read, update, and delete trips  
- JSON responses for all API endpoints  
- Input validation and error handling  
- Compatible with PostgreSQL  

## Technologies
- Python 3.11+  
- Flask 3.1.2  
- Flask SQLAlchemy 3.1.1  
- Flask-Migrate 4.1.0  
- Flask-Bcrypt 1.0.1  
- PostgreSQL  

## Setup & Installation

1. Clone the repository:
bash
git clone https://github.com/charlisse/travel_journal_api.git
cd travel_journal_api 


2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

3. install dependencies 
pip install -r requirements.txt

4. set environment variables (eg for postgreSQL)
export DATABASE_URL=postgresql://username:password@localhost:5432/travel_journal_db
export FLASK_APP=main.py
export FLASK_ENV=development

## Database Migration 

Initialise and migrate the database:
flask db init      # Only if first time
flask db migrate
flask db upgrade

## API Endpoints 

### Users 
- POST /users – Register a new user
- GET /users/<id> – Retrieve a user by ID

### Trips 
- GET /trips – List all trips
- POST /trips – Create a new trip
- GET /trips/<id> – Retrieve a trip by ID
- PUT /trips/<id> – Update a trip
- DELETE /trips/<id> – Delete a trip

## Example Requests
### Create user
curl -X POST http://127.0.0.1:5000/users \
-H "Content-Type: application/json" \
-d '{"username":"charli","email":"charli@example.com","password":"mypassword"}'

### Get Trips
curl http://127.0.0.1:5000/trips/

## Deployment 
This API can be deployed to Railway or any other cloud provider that supports Python & PostgreSQL. Ensure the environment variables match your production database configuration. 

## License
This project is licensed under the MIT License 

## Feedback 
I incorporated feedback at multiple stages of the project. Initially for my ERD, my Trips table used a one-to-many relationship with user_id. However following guidance from my teacher, I implemented a many-to-many relationship using a UserTrips junction table with a proper primary key. This change improved my database structure and functionality, demonstrating how I am quick to respond to feedback throughout development.

I also used feedback in project planning and workflow. I was overwhelmed to start and received suggestions to break development into smaller more manageable modules and use a consistant file structure. I then reorganised the project into seperate modules (main.py, routes/). This made the code easier to maintain, test and expand. 

Also used troubleshooting advice to improve the reliability of my database setup. Initially SQLite was casuing errors when testing the API so i adopted Docker to run a PostgreSQL container. This change ensured a consistent, isolated database environment that worked across different operating systems. By integrating Docker, i resolved persistent SQL issues and demonstrates that i adapted feedback and challenges through development. 