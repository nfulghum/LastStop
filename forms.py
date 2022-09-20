from unittest.loader import VALID_MODULE_NAME
from wsgiref import validate
from activities import ACTIVITY_CHOICES
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DecimalField, RadioField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange


def create_choices(list):
    """Create choice tuples to use as multiform choices."""

    result = []

    for choice in list:
        try:
            result.append((choice, choice.title()))
        except:
            pass
    return result


activity_choices = create_choices(ACTIVITY_CHOICES)


class UserAddForm(FlaskForm):
    """Form for adding users."""

    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image = StringField('(Optional) Image URL')
    bio = TextAreaField('Bio')
    phone = StringField('Phone', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = StringField('Zip', validators=[DataRequired()])


class UserEditForm(FlaskForm):
    """Form for editing users"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image = StringField('Image URL')
    bio = TextAreaField('Tell us about yourself')
    phone = StringField('Phone', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = StringField('Zip', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class GearPostForm(FlaskForm):
    """Gear Post form"""
    title = StringField('Title')
    condition = StringField('Condition')
    image = StringField('(Optional) Image URL')
    price = DecimalField('Price')
    description = TextAreaField('Description')
    activity = SelectField(
        'Event Activity', id='activities', choices=activity_choices)


class EventForm(FlaskForm):
    """Create a new meet up form"""

    title = StringField('Title', validators=[DataRequired()])
    exp_level = StringField('Experience Level', validators=[DataRequired()])
    trip_length = StringField('Trip Length', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    image = StringField('(Optional) Image URL')
    description = TextAreaField('Description', validators=[DataRequired()])
    activity = SelectField(
        'Event Activity', id='activities', choices=activity_choices)


class SearchForm(FlaskForm):
    """Form for searching for events/gear within a radius"""

    zip_code = IntegerField('Zip Code', validators=[NumberRange(
        min=00000, max=99999, message='Please enter a valid zip code.'), DataRequired()])
    radius = IntegerField('Radius in miles', default=10)
