from flask import render_template, url_for, request, flash, redirect
from dublinbikes import app
from dublinbikes.getdata import get_locations, get_current_station_data, get_all_station_data
from dublinbikes.forms import RegistrationForm, LoginForm
import json

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', locationdata=get_locations())


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created succesfully! Welcome, {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "cshort@tcd.ie" and form.password.data == "yes":
            flash(f"Logged in with email {form.email.data}", "success")
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
