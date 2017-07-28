import datetime

from project import db


# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(128), nullable=False)
#     email = db.Column(db.String(128), nullable=False)
#     active = db.Column(db.Boolean(), default=False, nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False)

#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#         self.created_at = datetime.datetime.utcnow()


CREATE TABLE voting_session(
    voting_session_id INT NOT NULL AUTO_INCREMENT,
    group_id INT NOT NULL,
    voting_status VARCHAR(10) DEFAULT NULL,
    #voting_result_id INT DEFAULT NULL, # not sure if we want this
    consensus_reached boolean DEFAULT 0,
    create_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
    update_date DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP, 
    PRIMARY KEY(voting_session_id)
);

class Group(db.Model):
    __tablename__ = "group"
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_name = db.Column(db.String(50), nullable=False)
    member_count = db.Column(db.Integer, default=0)
    create_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, group_name):
        self.group_name = group_name

class GroupDetails(db.Model):
    __tablename__ = "groupdetails"
    group_id = db.Column(db.Integer)
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

def VotingSession(db.Model):
    __tablename__ = "votingsession"
    group_id = db.Column(db.Integer)
    voting_status = db.Column(db.String)
    voting_result_id = 

