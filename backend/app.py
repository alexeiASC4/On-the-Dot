from collections import UserString
from db import db
from db import Event
from db import User
import json
from flask import Flask
from flask import request
import requests
from datetime import timedelta
from datetime import datetime
import os
import users_dao


app = Flask(__name__)
db_filename = "reminder.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(data, code=404):
    return json.dumps(data), code

def extract_token(request):
    """
    Helper function that extracts the token from the header of a request
    """
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return False, json.dumps({"Missing authorization header"})

    bearer_token = auth_header.replace("Bearer", "").strip()

    return True, bearer_token


@app.route("/")
@app.route("/api/user/")
def get_users():
    """
    Gets all users
    """
    return success_response({"users": [u.serialize() for u in User.query.all()] })


@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    """
    Get user by id
    """
    user = User.query.filter_by(id = user_id).first()
    if not user:
        return failure_response({"error": "user not found"})
    return success_response(user.serialize())


@app.route("/api/user/", methods = ["POST"])
def create_user():
    """
    Endpoint for registering a new user
    """
    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")

    if email is None or password is None:
        return failure_response({"Error": "Bad Request"}, 400)

    was_successful, user = users_dao.create_user(email, password)

    if not was_successful:
        return failure_response("User email already exists.")
    
    return success_response(
        {
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token
        }, 201
    )


@app.route("/api/users/login/", methods=["POST"])
def login():
    """
    Endpoint for logging in a user.
    """
    body = json.loads(request.data)
    email = body.get("email")
    password = body.get("password")

    if email is None or password is None:
        return failure_response("Missing email or password")

    was_successful, user = users_dao.verify_credentials(email, password)

    if not was_successful:
        return failure_response("Incorrect username or password.")

    return success_response(
        {
            "user_id": 1,
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token
        }, 201
    )


@app.route("/api/users/session/", methods=["POST"])
def update_session():
    """
    Endpoint for updating a user's session
    """
    was_successful, update_token = extract_token(request)

    if not was_successful:
        return update_token

    try:
        user = users_dao.renew_session(update_token)
    except Exception as e:
        return failure_response(f"Invalid update token: {str(e)}")

    return success_response(
        {
            "session_token": user.session_token,
            "session_expiration": str(user.session_expiration),
            "update_token": user.update_token
        }, 201
    )


@app.route("/api/users/logout/", methods=["POST"])
def logout():
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    user = users_dao.get_user_by_session_token(session_token)

    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")

    user.session_expiration = datetime.now()
    db.session.commit()

    return success_response({
        "message": "User Logged out."
    })


@app.route("/api/user/<int:user_id>/", methods = ["POST"])
def create_event(user_id):
    """
    Create an event for a user
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token
    print("Sess token " + session_token)
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")

    body = json.loads(request.data)
    name = body.get("name")
    #"Month DD YYYY H:MM[AM/PM]"
    dt = datetime.strptime(body.get("datetime"), '%b %d %Y %I:%M%p')
    duration = body.get("duration")
    location = body.get("location")
    arrival = body.get("arrival")
    if not name or not dt or not duration or not location or not arrival:
        return failure_response({"Error": "Bad Request"}, 400)

    new_event = Event(name=name, datetime=dt, duration=duration, location=location, arrival=arrival, user=user.id)
    user.events.append(new_event)
    db.session.add(new_event)
    db.session.commit()
    return success_response(new_event.serialize(), 201)
    
@app.route("/api/events/<int:user_id>/")
def get_time_sorted_events_by_user_id(user_id):
    """
    get all events related to a user by user id sorted by datetime of event
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token
    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")

    events = user.serialize()["events"]

    return success_response(sorted(events, key=lambda x: datetime.strptime(x['datetime'], '%b %d %Y %I:%M%p')))
    

@app.route("/api/events/<int:event_id>/", methods = ["DELETE"])
def delete_event(event_id):
    """
    delete event by id
    """
    was_successful, session_token = extract_token(request)

    if not was_successful:
        return session_token

    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return failure_response("Invalid session token")

    event = Event.query.filter_by(id = event_id).first()
    if not event:
        return failure_response("event not found")

    if event.users != user.id:
        return failure_response("Event does not belong to the user.")

    db.session.delete(event)
    db.session.commit()
    return success_response(event.serialize())


@app.route("/api/events/<int:event_id>/routes/", methods = ["POST"])
def get_routes(event_id):
    """
    Get an early arrival route
    """
    body = json.loads(request.data)
    event = Event.query.filter_by(id = event_id).first()
    if not event:
        return failure_response("event not found")
    destination = event.location
    arrival = event.arrival
    datetime = event.datetime
    tmp = datetime  - \
                timedelta(minutes = arrival)
    arrival_time = int(tmp.timestamp())

    origin = body.get("origin")
    if not origin:
        return failure_response({"error": "bad request"}, 400)
    api = os.environ.get("APIKEY")
    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=transit&arrival_time={arrival_time}&key={api}"
    payload={}
    headers={}
    response = requests.request("GET", url, headers=headers, data=payload)
    return (response.text)
   
"""
1. ADD AUTHENTICATION TOKEN
3. Postman testing
4. notifications and make changes to db file and get routes/departure times
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

