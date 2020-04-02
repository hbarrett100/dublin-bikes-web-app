from flask import render_template, url_for, request, flash, redirect
from dublinbikes import app, bcrypt
from dublinbikes.getdata import get_locations, get_current_station_data, get_all_station_data
from dublinbikes.users import get_password, add_user, add_favourite_station, get_favourite_stations, check_email, load_user
from dublinbikes.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

import json

@app.route('/')
@app.route('/home')
def home():
    print("home", current_user.is_authenticated)
    return render_template('home.html', locationdata=get_locations())


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods = ["GET", "POST"])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        add_user(form.email.data, hashed_pwd)

        flash(f"Account created succesfully with email {form.email.data}. Please log in to proceed", "success")

        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        flash(f"Already logged in with email {current_user.email}.", "success")
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.email.data)
        print(user)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Logged in with email {form.email.data}", "success")
            print("curr", current_user.is_authenticated)
            return redirect(url_for("home"))
        else:
            flash(f"Login failed, email and password do not match.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route('/query')
def query():
    # get the argument from the get request
    id = request.args.get('id')
    if id =="all":
        station_info = json.dumps(get_all_station_data())
    else:
        # invoke function to run sql query and store results
        station_info = json.dumps(get_current_station_data(id))
    return station_info
