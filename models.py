
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


def connect_db(app):
    """
    connect database to Flask app

    """

    db.app = app
    db.init_app(app)
