from collections import UserString
from db import db
from db import Event
from db import User
import json
from flask import Flask
from flask import request
import requests
from datetime import timedelta
import os


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


@app.route("/")
@app.route("/api/user/")
def get_users():
    """
    Gets all users
    """
    return success_response({"users": [u.serialize() for u in User.query.all()] })


@app.route("/api/user/<int:user_id>")
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
    Creates a user
    """
    body = json.loads(request.data)
    username = body.get("username")
    password = body.get("password")
    if not username or not password:
        return failure_response({"Error": "Bad Request"}, 400)
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


@app.route("/api/user/<int:user_id>", methods = ["POST"])
def create_event(user_id):
    """
    Create an event for a user
    """
    body = json.loads(request.data)
    name = body.get("name")
    datetime = body.get("datetime")
    duration = body.get("duration")
    location = body.get("location")
    arrival = body.get("arrival")
    Type = body.get("Type")
    if not name or not datetime or not duration or not location or not arrival:
        return failure_response({"Error": "Bad Request"}, 400)
    new_event = Event(name=name, datetime=datetime, duration=duration, location=location, arrival=arrival, users = user_id)
    db.session.add(new_event)
    db.session.commit()
    return success_response(new_event.serialize(), 201)
    

@app.route("/api/events/<int:event_id>", methods = ["DELETE"])
def delete_event(event_id):
    """
    delete event by id
    """
    event = Event.query.filter_by(id = event_id).first()
    if not event:
        return failure_response("event not found")
    db.session.delete(event)
    db.session.commit()
    return success_response(event.serialize())


@app.route("/api/events/<int:event_id>", methods = ["POST"])
def get_routes(event_id):
    """
    Get an early arrival route
    """
    body = json.loads(request.data)
    event = Event.query.filter_by(id = event_id).first()
    if not event:
        return failure_response("event not found")
    destination = event.get("location")
    arrival = event.get("arrival")
    datetime = event.get("datetime")
    tmp = datetime - \
                timedelta(minutes = arrival)
    arrival_time = datetime.timestamp(tmp)
    origin = body.get("origin")
    if not origin:
        return failure_response({"error": "bad request"}, 400)
    api = os.environ.get("APIKEY")    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=transit&arrival_time={arrival_time}&key={api}"
    payload={}
    headers={}
    response = requests.request("GET", url, headers=headers, data=payload)
    return success_response(response.text)
   
"""
1. ADD AUTHENTICATION TOKEN
2. env file (api key for google)
3. Postman testing
4. notifications and make changes to db file and get routes/departure times
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

