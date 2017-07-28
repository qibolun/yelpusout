import datetime

from project import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.datetime.utcnow()

class Group(db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupname = db.Column(db.String(128), nullable=False)
    location_latitude = db.Column(db.Float, nullable=True)
    location_longitude = db.Column(db.Float, nullable=True)
    radius = db.Column(db.Integer, nullable=True)
    price = db.Column(db.String(128), nullable=True)
    openat = db.Column(db.Integer, nullable=True)
    categories = db.Column(db.String(128), nullable=True)
    member_number = db.Column(db.Integer, default=0)

    def __init__(self, groupname, location, radius, price, openat, categories):
        self.groupname = groupname
        self.location_latitude = location['latitude']
        self.location_longitude = location['longitude']
        self.radius = radius
        self.price = price
        self.openat = openat
        self.categories = categories
