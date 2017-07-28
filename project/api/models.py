import datetime

from project import db

# We're probably not gonna use 'Users'
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
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(50), nullable=False)
    member_count = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, group_name):
        self.group_name = group_name

class GroupDetails(db.Model):
    __tablename__ = "groupdetails"
    group_id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    radius = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(20), nullable=False)
    open_at = db.Column(db.Integer)
    categories = db.Column(db.String(20))

    def __init__(self, group_id, latitude, longitude, radius, price, open_at, categories):
        self.group_id = group_id
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.price = price
        self.open_at = open_at
        self.categories = categories

class VotingSession(db.Model):
    __tablename__ = "votingsession"
    voting_session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer)
    voting_status = db.Column(db.String)
    vote_count = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, group_id, voting_status):
        group_id = group_id
        voting_status = voting_status
