from flask import render_template, url_for, request, flash, redirect
from dublinbikes import app, bcrypt
from dublinbikes.getdata import get_locations, get_current_station_data, get_all_station_data
from dublinbikes.users import get_password, add_user, add_favourite_station, get_favourite_stations, check_email, load_user
from dublinbikes.forms import RegistrationForm, LoginForm, UpdateEmail, UpdatePassword
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
    if current_user.is_authenticated:
        flash(f"Already logged in with email {current_user.email}. Please log out to register another account.", "danger")
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        add_user(form.email.data, hashed_pwd)

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
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

    if email_form.validate_on_submit():
        flash(f"Email updated.", "success")
        current_user.update_email(email_form.email.data)
        return redirect(url_for("account"))
    return render_template("account.html", title="Account", email_form=email_form, password_form=password_form)


@app.route('/updatepwd', methods=["GET", "POST"])
def updatepwd():
    if not current_user.is_authenticated:
        flash(f"You must log in to access account settings.", "danger")

    email_form = UpdateEmail()
    password_form = UpdatePassword()

    if password_form.validate_on_submit():
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


