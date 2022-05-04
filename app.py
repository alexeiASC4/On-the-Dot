from collections import UserString
from db import db
from db import Event
from db import Asset
import json
from flask import Flask
from flask import request
import requests
from datetime import datetime
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
@app.route("/api/events/")
def get_courses():
    """
    Gets all events
    """
    return success_response({"events": [e.serialize() for e in Event.query.all()] })

@app.route("/api/events/", methods = ["POST"])
def create_event():
    """
    Create an event
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
    new_event = Event(name=name, datetime=datetime, duration=duration, location=location, arrival=arrival, Type=Type)
    db.session.add(new_event)
    db.session.commit()
    return success_response(new_event.serialize(), 201)

@app.route("/api/events/<int:event_id>")
def get_event_id(event_id):
    """
    Gets course by id
    """
    course = Event.query.filter_by(id = event_id).first()
    if not course:
        return failure_response({"error":"course not found"})
    return success_response(course.serialize())

@app.route("/api/events/<int:event_id>", methods = ["DELETE"])
def delete_event(event_id):
    """
    delete event by id
    """
    event = Event.query.filter_by(id = event_id).first()
    if not event:
        return failure_response("course not found")
    db.session.delete(event)
    db.session.commit()
    return success_response(event.serialize())

@app.route("/api/events/<int:event_id>", methods = ["POST"])
def get_routes(event_id):
    body = json.loads(request.data)
    event = Event.query.filter_by(id = event_id).first()
    destination = event.get("location")
    arrival = event.get("arrival")
    origin = body.get("origin")
    departure_time = ""
    api = os.environ.get("APIKEY")    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode=transit&departure_time={departure_time}&key={api}"
    payload={}
    headers={}
    response = requests.request("GET", url, headers=headers, data=payload)
    return success_response(response.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

