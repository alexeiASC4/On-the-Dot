from calendar import day_abbr
from unicodedata import name, numeric
from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


class User(db.Model):
    """
    User model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable= False)
    password = db.Column(db.String, nullable = False)
    events = db.relationship("Event", cascade = "delete")
    
    def __init__(self, **kwargs):
        """
        Initializes users model
        """
        self.username = kwargs.get("username", "")
        self.password = kwargs.get("password", "")
        self.events = []
    
    def serialize(self):
        """
        Returns dictionary in organized format
        """
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "events": [e.simp_serialize() for e in self.events]
        }

    def simp_serialize(self):
        """
        Simple serialize
        """
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }

class Event(db.Model):
    """
    Event model
    """
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    datetime = db.Column(db.DateTime, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    location = db.Column(db.String, nullable = False)
    arrival = db.Column(db.Integer, nullable = False)
    users = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, **kwargs):
        """
        Initializes Event class
        """
        self.name = kwargs.get("name", "")
        self.datetime = kwargs.get("datetime", "")
        self.duration = kwargs.get("duration", "")
        self.location = kwargs.get("location", "")
        self.arrival = kwargs.get("arrival", 0)
        self.users = kwargs.get("user_id", "")

    def serialize(self):
        """
        Return dictionary in organize format
        """
        return {
            "id": self.id,
            "name": self.name,
            "datetime": self.datetime,
            "duration": self.duration,
            "location": self.location,
            "arrival": self.arrival
        }



