
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=False)

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True)

    phone = db.Column(
        db.Text,
        nullable=False)

    username = db.Column(
        db.Text, nullable=False,
        unique=True)

    bio = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False)

    image = db.Column(
        db.Text,
        default="""NEED TO ADD A DEFAULT IMG""")

    city = db.Column(
        db.Text,
        nullable=False)

    state = db.Column(
        db.Text,
        nullable=False)

    zip = db.Column(
        db.Integer,
        nullable=False)

    gear = db.relationship('GearPost')

    event = db.relationship('Event')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, name, username, email, password, bio, image, phone, city, state, zip):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            name=name,
            username=username,
            email=email,
            password=hashed_pwd,
            bio=bio,
            image=image,
            phone=phone,
            city=city,
            state=state,
            zip=zip,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class GearPost(db.Model):
    """Gear posted by users for sell, rent, trade"""

    __tablename__ = 'gearposts'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.Text,
        nullable=False
    )

    condition = db.Column(
        db.Text,
        nullable=False)

    image = db.Column(
        db.Text,
        default="""NEED TO ADD A DEFAULT IMG""")

    price = db.Column(
        db.Float,
        nullable=False)

    description = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE')
    )

    activity_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'activities.id',
            ondelete='CASCADE')
    )

    user = db.relationship('User')


class Activity(db.Model):
    """Activities available in Last Stop"""

    __tablename__ = 'activities'

    id = db.Column(
        db.Integer,
        primary_key=True)

    name = db.Column(
        db.Text,
        nullable=False,
        unique=True)


class Event(db.Model):
    """User adventure post"""

    __tablename__ = 'events'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.Text,
        nullable=False
    )

    exp_level = db.Column(
        db.Text,
        nullable=False
    )

    trip_length = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.Text,
        nullable=False
    )

    image = db.Column(
        db.Text,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE')
    )

    activity_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'activities.id',
            ondelete='CASCADE'
        )
    )

    user = db.relationship('User')


def connect_db(app):
    """
    connect database to Flask app

    """

    db.app = app
    db.init_app(app)
