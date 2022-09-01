from unittest.loader import VALID_MODULE_NAME
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FloatField, DateField
from wtforms.validators import DataRequired, Email, Length


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

    condition = StringField('Condition')
    image = StringField('(Optional) Image URL')
    price = FloatField('Price')
    description = TextAreaField('Description')


class MeetUpForm(FlaskForm):
    """Create a new meet up form"""

    date = DateField('Start Date', format='%m/%d/%Y',
                     validators=[DataRequired()])
    exp_level = StringField('Experience Level', validators=[DataRequired()])
    trip_length = StringField('Trip Length', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    image = StringField('(Optional) Image URL')
    description = TextAreaField('Description', validators=[DataRequired()])
