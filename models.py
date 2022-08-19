
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    img_url = db.Column(db.Text, default="""NEED TO ADD A DEFAULT IMG""")

    messages = db.relationship('Message')

    # need to add in bcrypt functionality


class Message(db.Model):
    """messages between users"""

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(140), nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User')


class GearPost(db.model):
    """Gear posted by users for sell, rent, trade"""

    id = db.Column(db.Integer, primary_key=True)

    condition = db.Column(db.Text, nullable=False)

    img_url = db.Column(db.Text, default="""NEED TO ADD A DEFAULT IMG""")

    price = db.Column(db.Float, nullable=False)

    location = db.Column(db.Text, nullable=False)

    delivery_method = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)

    activity_id = db.Column(db.Integer, db.ForeignKey(
        'activities.id', ondelete='CASCADE'), nullable=False)


class Likes(db.Model):
    """User likes (messages, gear, trips, etc)"""


class Groups(db.Model):
    """User groups"""


class Activity(db.Model):
    """Activities available in Last Stop"""

    id = db.Column(db.Integer, primary_key=True)

    activity_name = db.Column(db.Text, nullable=False, unique=True)


class AdventurePost(db.Model):
    """User adventure post"""

    id = db.Column(db.Integer, primary_key=True)

    # date = db.Column() need to see if this is integer or something else

    exp_level = db.Column(db.Text, nullable=False)

    duration = db.Column(db.Integer, nullable=False)

    num_spots = db.Column(db.Integer, nullable=False)

    # location = db.Column(db.Text, nullable=False) how to implement the api for this

    img_url = db.Column(db.Text, default="""Need to add a default img""")


def connect_db(app):
    """
    connect database to Flask app

    """

    db.app = app
    db.init_app(app)
