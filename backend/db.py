from calendar import day_abbr
from unicodedata import name, numeric
from flask_sqlalchemy import SQLAlchemy
import datetime
import bcrypt
import hashlib
import os


db = SQLAlchemy()


class User(db.Model):
    """
    User model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    # User Information
    email = db.Column(db.String, nullable= False, unique=True)
    password_digest = db.Column(db.String, nullable = False)

    # Session information
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    events = db.relationship("Event", cascade = "delete")
    
    def __init__(self, **kwargs):
        """
        Initializes users model, including adding salt and hashing the password.
        """
        self.email = kwargs.get("email")
        self.password_digest = bcrypt.hashpw(kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13))
        self.events = []
        
    
    def serialize(self):
        """
        Returns dictionary in organized format
        """
        return {
            "id": self.id,
            "email": self.email,
            "events": [e.serialize() for e in self.events]
        }

    def simp_serialize(self):
        """
        Simple serialize
        """
        return {
            "id": self.id,
            "email": self.email
        }

    def _urlsafe_base_64(self):
        """
        Randomly generates hashed tokens (used for session/update tokens)
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        """
        Renews the session by creating a new session token (1 day experation) 
        and a new update_token.
        """
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        """
        Verifies the password of a user.
        """
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    def verify_session_token(self, session_token):
        """
        Verifies the session token of a user
        """
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        """
        Verifies the update token of a user
        """
        return update_token == self.update_token


class Event(db.Model):
    """
    Event model
    """
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    datetime = db.Column(db.Integer, nullable = False)
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



