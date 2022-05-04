from calendar import day_abbr
from unicodedata import name, numeric
from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


association_table = db.Table(
    "association",
    db.Column("event_id", db.Integer. db.ForeignKey("events.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

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
    origin = db.Column(db.String, nullable = False)
    arrival = db.Column(db.Integer, nullable = False)
    users = db.relationship("User", secondary = association_table, back_populates = "events")

    def __init__(self, **kwargs):
        """
        Initializes Event class
        """
        self.name = kwargs.get("name", "")
        self.datetime = kwargs.get("datetime", "")
        self.duration = kwargs.get("duration", "")
        self.location = kwargs.get("location", "")
        self.origin = kwargs.get("origin", "current_location")
        self.arrival = kwargs.get("arrival", 0)
        self.Type = kwargs.get("Type", "")
        self.days = kwargs.get("days", "")
        self.users = []

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
            "arrival": self.arrival,
            "Type": self.Type,
            "days": self.days,
            "users": [u.simple_serialize() for u in self.users]
        }

    def simp_serialize(self):
        """
        Simple serialize
        """
        return {
            "id": self.id,
            "name": self.name,
            "datetime": self.datetime,
            "duration": self.duration,
            "location": self.location,
            "arrival": self.arrival,
            "Type": self.Type,
            "days": self.days
        }

class User(db.Model):
    """
    User model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable= False)
    password = db.Column(db.String, nullable = False)
    events = db.relationship("Event", secondary= association_table, back_populates = "users")
    
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
            "events": [e.simple_serialize() for e in self.events]
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



# class Asset(db.Model):
#     """
#     Asset model
#     """
#     __tablename__ = "assets"
#     id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     base_url = db.Column(db.String, nullable = False)
#     salt = db.Column(db.String, nullable= False)
#     extension = db.Column(db.String, nullable = False)
#     height = db.Column(db.Integer, nullable = False)
#     width = db.Column(db.Integer, nullable = False)
#     created_at = db.Column(db.DateTime, nullable = False)
#     event = db.Column(db.Integer, db.ForeignKey("events.id"))

#     def __init__(self, **kwargs):
#         """
#         Iniitializes asset model
#         """
#         self.create(kwargs.get("image_data", ""))
#         self.event_id = kwargs.get("event_id", "")

#     def create(self, image_data):
#         """
#         Given an image in base64 form, does the following:
#         1. Rejects the image if it is not a support filetype
#         2. Generates a random string for the image filname
#         3. Decodes the image and attempts to uplaod it to AWS
#         """
#         try:
#             ext = guess_extension(guess_type(image_data)[0])[1:]
        
#             if ext not in EXTENSIONS:
#                 raise Exception(f"Unsupported file type:{ext}")

#             salt = "".join(
#                 random.SystemRandom().choice(
#                     string.ascii_uppercase + string.digits
#                 )
#                 for _ in range(16)
#             )

#             img_str = re.sub("^data:image/.+;base64", "", image_data)
#             img_data = base64.b64code(img_str)
#             img = Image.open(BytesIO(img_data))

#             self.base_url = S3_BASE_URL
#             self.salt = salt
#             self.extension = ext
#             self.width = img.width 
#             self.height = img.height
#             self.create_at = datetime.datetime.now()

#             img_filename = f"{self.salt}.{self.extension}"
#             self.upload(img, img_filename)

#         except Exception as e:
#             print(e)
        

#     def upload(self, img, img_filename):
#         """
#         Attempts to upload the image to the specified bucket
#         """
#         try:
#             img_temploc = f"{BASE_DIR}/{img_filename}"
#             img.save(img_temploc)

#             s3_client = boto.client("s3")
#             s3_client.upload_file(img_temploc, S3_BUCKET_NAME, img_filename)

#             s3_resource = boto.resource("s3")
#             object_acl = s3_resource.ObjectAcl(S3_BUCKET_NAME, img_filename)
#             object_acl.put(ACL="public-read")

#             os.remove(img_temploc)

#         except Exception as e:
#             print(e)

#     def serialize(self):
#         """
#         Serializes an Asset Object 
#         """
#         return {
#             "url": f"{self.base_url}/{self.salt}.{self.extension}",
#             "created_at": str(self.create_at)
#         }