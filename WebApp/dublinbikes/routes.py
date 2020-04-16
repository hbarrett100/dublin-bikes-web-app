
from flask import render_template, url_for, request, flash, redirect
from dublinbikes import app, bcrypt
from dublinbikes.getdata import * 
from dublinbikes.users import * 
from dublinbikes.forms import RegistrationForm, LoginForm, UpdateEmail, UpdatePassword, SendConfirmEmail, DeleteAccount, ResetPasswordForm, ForgotPassword
from flask_login import login_user, current_user, logout_user, login_required
from itsdangerous import URLSafeTimedSerializer
import json


# ================================== PAGE ROUTES ==================================
# These routes return a rendered HTML page

# =========== HOME ===========
@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        stations = current_user.stations
    else:
        stations = 0
    
    email_not_confirmed(current_user)

    return render_template('home.html', locationdata=get_locations(), stations=stations)



# =========== ABOUT ===========
@app.route('/about')
def about():
    email_not_confirmed(current_user)
    return render_template('about.html', title='About')



# =========== PRIVACY POLICY ===========
@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html', title='Privacy Policy')



# =========== REGISTER ===========
@app.route("/register", methods = ["GET", "POST"])
def register():
    # Check is user is logged in, if so they can't access register route
    if current_user.is_authenticated:
        flash(f"Already logged in with email {current_user.email}. Please log out to register another account.", "danger")
        return redirect(url_for("home"))

    form = RegistrationForm()

    # Check if registration was valid, if so redirect to login page
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        add_user(form.email.data, hashed_pwd)
        send_confirm_email(form.email.data)
        flash(
            f"Registration successful, a confirmation email has been sent to {form.email.data} Please login to proceed.", "success")
        return redirect(url_for("login"))

    # Otherwise display register form
    return render_template("register.html", title="Register", form=form)




# =========== LOGIN ===========
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





# =========== ACCOUNT ===========
@app.route('/account', methods=["GET", "POST"])
def account():
    # Check is user is logged in, if not they can't access login route
    if not current_user.is_authenticated:
        flash(f"You must log in to access account settings.", "danger")
        return redirect(url_for("home"))

    # Prefixes are used to prevent multiple elements having the same ID when rendered as HTML
    email_form = UpdateEmail(prefix="email")
    password_form = UpdatePassword(prefix="pwd")
    send_confirm_form = SendConfirmEmail(prefix = "conf-email")
    del_acc_form = DeleteAccount(prefix="del-acc")

    # if password_form.submit.data and password_form.validate():
    #     flash(f"Password updated.", "success")
    #     return redirect(url_for("account"))
    email_not_confirmed(current_user)
    return render_template("account.html", title="Account", email_form=email_form, password_form=password_form, send_confirm_form=send_confirm_form, del_acc_form=del_acc_form)


# =========== FORGOT PASSWORD ===========
@app.route('/reset', methods=["GET", "POST"])
def reset():
    form = ForgotPassword()
    if form.validate_on_submit():

        user = load_user(form.email.data)

        if user.emailvalidated:
            send_password_reset_email(user.email)
            flash('Please check your email for a password reset link.', 'success')
        else:
            flash(
                'Your email address must be confirmed before attempting a password reset.', 'danger')
        return redirect(url_for('login'))

    return render_template('password_reset_email.html', form=form)




# ================================== USER ROUTES ==================================
# These are related to the login functionality and allow the user to
# update their info

# =========== LOG OUT ===========
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


# =========== UPDATE EMAIL ===========
@app.route('/updateemail', methods=["GET", "POST"])
def updateemail():
    if not current_user.is_authenticated:
        flash(f"You must log in to access account settings.", "danger")
    
    email_form = UpdateEmail(prefix="email")
    password_form = UpdatePassword(prefix="pwd")
    send_confirm_form = SendConfirmEmail(prefix="conf-email")
    del_acc_form = DeleteAccount(prefix="del-acc")

    # Check that the form is valid and input password matches stored password
    if email_form.validate_on_submit() and bcrypt.check_password_hash(current_user.password, email_form.password.data):
        current_user.update_feature(email_form.email.data, "email")

        # email update means email is no longer confirmed, so the confirmation emaail is resent
        current_user.update_feature(0, "confirm")
        send_confirm_email(email_form.email.data)

        # The login manager uses the email as the identifier of the current_user,
        # so the user is automically logged out and logged in the new email
        logout_user()
        user = load_user(email_form.email.data)
        login_user(user)

        flash(f"Email updated, a confirmation email has been sent.", "success")
        return redirect(url_for("account"))
    return render_template("account.html", title="Account", email_form=email_form, password_form=password_form, send_confirm_form=send_confirm_form, del_acc_form=del_acc_form)


# =========== UPDATE PASSWORD ===========
@app.route('/updatepwd', methods=["GET", "POST"])
def updatepwd():
    if not current_user.is_authenticated:
        flash(f"You must log in to access account settings.", "danger")

    email_form = UpdateEmail(prefix="email")
    password_form = UpdatePassword(prefix="pwd")
    send_confirm_form = SendConfirmEmail(prefix="conf-email")
    del_acc_form = DeleteAccount(prefix="del-acc")

    # Check that the form is valid and input password matches stored password
    if password_form.validate_on_submit() and bcrypt.check_password_hash(current_user.password, password_form.old_password.data):
        # hash the new password and update the user's info
        hashed_pwd = bcrypt.generate_password_hash(password_form.new_password.data).decode("utf-8")
        current_user.update_feature(hashed_pwd, "password")
        flash(f"Password updated.", "success")
        return redirect(url_for("account"))
    return render_template("account.html", title="Account", email_form=email_form, password_form=password_form, send_confirm_form=send_confirm_form, del_acc_form=del_acc_form)


# =========== SEND CONFIRMATION EMAIL ===========
@app.route('/confirmemail', methods=["GET", "POST"])
def confirmemail():
    send_confirm_email(current_user.email)
    flash(f"Confirmation email sent.", "success")
    return redirect(url_for("account"))


# =========== DELETE ACCOUNT ===========
@app.route('/deleteaccount', methods=["GET", "POST"])
def deleteaccount():

    del_acc_form = DeleteAccount(prefix="del-acc")

    if del_acc_form.validate_on_submit() and bcrypt.check_password_hash(current_user.password, del_acc_form.password.data):

        current_user.delete_account()
        logout_user()
        flash(f"Account Deleted.", "success")
        return redirect(url_for("home"))
    else:
        flash(f"Password did not match.", "danger")
    return redirect(url_for("account"))


# =========== CONFIRM EMAIL USING TOKEN ===========
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        flash(f"Something went wrong.", "danger")
        return redirect(url_for('home'))

    user = load_user(email)

    user.update_feature(1, "emailvalidated")
    flash(f"Your email has been confirmed, thank you.", "success")
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))


# =========== RESET PASSWORD USING TOKEN ===========
@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(
            app.config['SECRET_KEY'])
        email = password_reset_serializer.loads(
            token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('login'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = load_user(email=email)
        hashed_pwd = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")

        user.update_feature(hashed_pwd, "password")

        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password_with_token.html', form=form, token=token)


# =========== UPDATE FAVOURITED STATIONS LIST ===========
@app.route("/addstation", methods=["GET", "POST"])
def addstation():
    # Check is user is logged in, if so they can't access addstation route
    if not current_user.is_authenticated:
        flash(f"You must be logged in to add stations to favourites", "danger")
        return redirect(url_for("home"))
    action = request.form['action'] + "_station"
    station_id = request.form['id']
    current_user.update_feature(station_id, action)
    return json.dumps(current_user.stations)




# ================================== QUERY ROUTES ==================================
# These retrieve bike and weather data from the db or json files

# =========== GET CURRENT AVAILABILTY DATA ===========
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


# =========== GET HOURLY OR DAILY AVERAGE DATA  ===========
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


# =========== GET AVAILABILITY PREDICTIONS FOR A STATION ===========
@app.route('/predictions')
def predictions():
    id = request.args.get('id')
    prediction_info = json.dumps(get_prediction(id))
    return prediction_info

# =========== GET WEATHER FORECAST ===========
@app.route('/weather')
def weather():
    day = int(request.args.get('day'))
    hour = int(request.args.get('hour'))
    weather_info = json.dumps(get_hourly_forecast(day,hour))
    return weather_info



