
from flask import render_template, url_for, request, flash, redirect
from dublinbikes import app, bcrypt
from dublinbikes.getdata import * # import get_locations, get_current_station_data, get_all_station_data, 
from dublinbikes.users import get_password, add_user, add_favourite_station, get_favourite_stations, check_email, load_user
from dublinbikes.forms import RegistrationForm, LoginForm, UpdateEmail, UpdatePassword
from flask_login import login_user, current_user, logout_user, login_required
import json

@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        stations = current_user.stations
    else:
        stations = "[]"
        
    return render_template('home.html', locationdata=get_locations(), stations=stations)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods = ["GET", "POST"])
def register():
    # Check is user is logged in, if so they can't access regiter route
    if current_user.is_authenticated:
        flash(f"Already logged in with email {current_user.email}. Please log out to register another account.", "danger")
        return redirect(url_for("home"))

    form = RegistrationForm()

    # Check if registration was valid, if so redirect to login page
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        add_user(form.email.data, hashed_pwd)
        flash(f"Registration successful. Please login to proceed.", "success")
        return redirect(url_for("login"))

    # Otherwise display register form
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Check is user is logged in, if so they can't access login route
    if current_user.is_authenticated:
        flash(f"Already logged in with email {current_user.email}.", "success")
        return redirect(url_for("home"))

    form = LoginForm()

    # Check if the login for is filled in correctly
    if form.validate_on_submit():
        user = load_user(form.email.data)
        print(user)
        # Check if user and password match
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Log the user in and redirect to home page
            login_user(user, remember=form.remember.data)
            flash(f"Logged in with email {form.email.data}", "success")
            print("curr", current_user.is_authenticated)
            return redirect(url_for("home"))
        else:
            flash(f"Login failed, email and password do not match.", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/account', methods=["GET", "POST"])
def account():
    if not current_user.is_authenticated:
        flash(f"You must log in to access account settings.", "danger")
        return redirect(url_for("home"))
    email_form = UpdateEmail()
    password_form = UpdatePassword()



    if password_form.submit.data and password_form.validate():
        flash(f"Password updated.", "success")
        return redirect(url_for("account"))

    return render_template("account.html", title="Account", email_form=email_form, password_form=password_form)


@app.route('/updateemail', methods=["GET", "POST"])
def updateemail():
    if not current_user.is_authenticated:
        flash(f"You must log in to access account settings.", "danger")
    
    email_form = UpdateEmail()
    password_form = UpdatePassword()

    if email_form.validate_on_submit() and bcrypt.check_password_hash(current_user.password, email_form.password.data):
        current_user.update_feature(email_form.email.data, "email")
        logout_user()
        user = load_user(email_form.email.data)
        login_user(user)
        flash(f"Email updated.", "success")
        return redirect(url_for("account"))
    return render_template("account.html", title="Account", email_form=email_form, password_form=password_form)


@app.route('/updatepwd', methods=["GET", "POST"])
def updatepwd():
    if not current_user.is_authenticated:
        flash(f"You must log in to access account settings.", "danger")

    email_form = UpdateEmail()
    password_form = UpdatePassword()

    if password_form.validate_on_submit() and bcrypt.check_password_hash(current_user.password, password_form.old_password.data):
        
        hashed_pwd = bcrypt.generate_password_hash(password_form.new_password.data).decode("utf-8")
        current_user.update_feature(hashed_pwd, "password")
        flash(f"Password updated.", "success")
        return redirect(url_for("account"))
    return render_template("account.html", title="Account", email_form=email_form, password_form=password_form)


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


@app.route("/addstation", methods=["GET", "POST"])
def addstation():
    # Check is user is logged in, if so they can't access addstation route
    if not current_user.is_authenticated:
        flash(f"You must be logged in to add stations to favourites", "danger")
        return redirect(url_for("home"))
    action = request.form['action'] + "_station"
    station_id = request.form['id']
    print(station_id, action)
    print(current_user.stations)
    current_user.update_feature(station_id, action)
    email = current_user.email
    logout_user()
    user = load_user(email)
    login_user(user)
    print(type(current_user.stations))
    return json.dumps(current_user.stations)


@app.route('/averages')
def averages():
    # get the argument from the get request
    id = request.args.get('id')
    day = request.args.get('day')
    if day =="all":
        average_info = json.dumps(get_weekly_data(id))
    else:
        # invoke function to run sql query and store results
        average_info = json.dumps(get_hourly_data_by_day(day, id))
    return average_info

@app.route('/predictions')
def predictions():
    id = request.args.get('id')
    prediction_info = json.dumps(get_prediction(id))
    return prediction_info

