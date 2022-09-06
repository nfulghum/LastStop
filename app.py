import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import User, GearPost, Activity, Event, connect_db, db
from forms import GearPostForm, LoginForm, EventForm, UserAddForm, UserEditForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///laststop'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "shhhhh")
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def index():
    return render_template('home.html')


############################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/register', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                name=form.name.data,
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                bio=form.bio.data,
                image=form.image.data or User.image.default.arg,
                phone=form.phone.data,
                city=form.city.data,
                state=form.state.data,
                zip=form.zip.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/register.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    session.pop(CURR_USER_KEY)
    flash("Logged out")

    return redirect('/')

##########################################
# User routes


@app.route('/users/<int:user_id>')
def users_profile(user_id):
    """Show users profile"""

    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user=user)


@app.route('/users/edit', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image = form.image.data
            user.bio = form.bio.data
            user.phone = form.phone.data
            user.city = form.city.data
            user.state = form.state.data
            user.zip = form.zip.data

            db.session.commit()
            return redirect(f"/{g.user.id}")

        flash("Wrong password, try again", "danger")

    return render_template('users/edit.html', form=form, user_id=user.id)

###########################################
# Gear routes


@app.route('/gear/gear-list')
def show_gear():
    """Show gear list"""

    gear = GearPost.query.all()

    return render_template('/gear/gear_list.html', gear=gear)


@app.route('/gear/<int:gear_id>', methods=["GET"])
def single_gear(gear_id):
    """Show single gear post if clicked on"""

    gear = GearPost.query.get(gear_id)

    return render_template('/gear/single_gear.html', gear=gear)


@app.route('/gear/new_gear', methods=["GET", "POST"])
def add_gear():
    """Add a gear post"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')

    form = GearPostForm()

    if form.validate_on_submit():
        gear = GearPost(
            title=form.title.data,
            condition=form.condition.data,
            image=form.image.data,
            price=form.price.data,
            description=form.description.data
        )
        g.user.gear.append(gear)
        db.session.commit()

        return redirect(f'/gear/gear-list')

    return render_template('/gear/new_gear.html', form=form)


@app.route('/gear/<int:gear_id>/delete', methods=["POST"])
def gear_delete(gear_id):
    """Delete Gear Post"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')

    gear = GearPost.query.get(gear_id)
    db.session.delete(gear)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")


###########################################
# Meet up routes

@app.route('/meetups/events')
def show_events():
    """Show list of meet ups"""

    event = Event.query.all()

    return render_template('/meetups/events_list.html', event=event)


@app.route('/meetups/<int:event_id>', methods=["GET"])
def single_event(event_id):
    """Show single event post if clicked on"""

    event = Event.query.get(event_id)

    return render_template('/meetups/single_event.html', event=event)


@app.route('/meetups/new_event', methods=["GET", "POST"])
def add_event():
    """Add a event post"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')

    form = EventForm()

    if form.validate_on_submit():
        event = EventForm(
            title=form.title.data,
            exp_level=form.exp_level.data,
            image=form.image.data,
            trip_length=form.trip_length.data,
            description=form.description.data,
            location=form.location.data
        )

        g.user.event.append(event)
        db.session.commit()

        return redirect(f'/meetups/events')

    return render_template('/meetups/new_event.html', form=form)


@app.route('/meetups/<int:event_id>/delete', methods=["POST"])
def event_delete(event_id):
    """Delete Event Post"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')

    event = Event.query.get(event_id)
    db.session.delete(event)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")
