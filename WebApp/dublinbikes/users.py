

# This file contains the User class and other functions related to the creation and updating a user account

from dublinbikes import login_manager, mail, app
from dublinbikes.getdata import connect_to_db
from dublinbikes.config import *
from flask_login import UserMixin
from flask_mail import Message
from flask import render_template, url_for, flash
from itsdangerous import URLSafeTimedSerializer
import mysql.connector
import json

# ====== ADDING A USER ======

# Add a new user to the database using their email and encrypted password
def add_user(email, password):
    try:
        # Connect to the RDS database
        mydb = connect_to_db()

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('add_user', (email, password, ))
        mydb.commit()

        print(mycursor.rowcount)
    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

    mycursor.close()
    mydb.close()
    

# Check to see if an email already exists in the database
def check_email(email):
    try:
        # Connect to the RDS database
        mydb = connect_to_db()

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('check_if_email_exists', [email, ])

        results = mycursor.stored_results()

    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

    for result in results:
        email_exists = result.fetchall()[0][0]

    mycursor.close()
    mydb.close()

    return email_exists


# ====== USER CLASS ======

# This User class is used for the login functionality.
# When a user is logged in, an instance of this class is created and called current_user
# The user's data can then easily be accessed and updated
class User(UserMixin):
    def __init__(self, email):
        try:
            # Connect to the RDS database
            mydb = connect_to_db()

            mycursor = mydb.cursor()

            # called mysql stored procedure giving email as an argument
            mycursor.callproc('get_user_details_by_email', [email, ])

            results = mycursor.stored_results()

        except mysql.connector.Error as err:

            print("SOMETHING WENT WRONG:", err)

        for result in results:
            u = result.fetchall()[0]
            self.email = u[0]
            self.password = u[1]
            self.stations = json.loads(u[2])
            self.emailvalidated = u[3]
            print(self.stations)

        mycursor.close()
        mydb.close()

    def get_id(self):
        return self.email

    def delete_account(self):
        try:
            # Connect to the RDS database
            mydb = connect_to_db()

            mycursor = mydb.cursor()
            mycursor.callproc('delete_user', [self.email, ])

            mydb.commit()
        except mysql.connector.Error as err:

            print("SOMETHING WENT WRONG:", err)

        mycursor.close()
        mydb.close()

    def update_feature(self, data, feature):
        try:
            # Connect to the RDS database
            mydb = connect_to_db()

            mycursor = mydb.cursor()
            # called mysql stored procedure giving email as an argument
            if feature == "email":
                mycursor.callproc('update_email', [self.email, data])

            elif feature == "password":
                self.password = data
                mycursor.callproc('update_password', [self.email, data])

            elif feature == "emailvalidated":
                self.emailvalidated = data
                mycursor.callproc('update_emailvalidated', [self.email, data])

            elif feature == "add_station":
                self.stations.append(data)
                mycursor.callproc('update_stations', [
                                  self.email, json.dumps(self.stations)])

            elif feature == "remove_station":
                if data in self.stations:
                    self.stations.remove(data)
                mycursor.callproc('update_stations', [
                                  self.email, json.dumps(self.stations)])

            mydb.commit()
        except mysql.connector.Error as err:

            print("SOMETHING WENT WRONG:", err)

        mycursor.close()
        mydb.close()

    def __repr__(self):
        return f"{self.email}, {self.password}, {self.stations}"


# The login manager uses this function to create an instance of User
@login_manager.user_loader
def load_user(email):
    if(check_email(email)):
        return User(email)
    else:
        return None


# ====== EMAIL FUNCTIONS ======

# Render and send a confirmation email using a time sensitive token
def send_confirm_email(email):
    subject = "Confirm your email"

    ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

    token = ts.dumps(email, salt='email-confirm-key')

    confirm_url = url_for(
        'confirm_email',
        token=token,
        _external=True)

    msg = Message(subject,
                  recipients=[email])

    msg.html = render_template(
        '/activate.html',
        confirm_url=confirm_url)

    mail.send(msg)


# Render and send a password reset email
def send_password_reset_email(email):

    subject = 'Password Reset Requested'

    password_reset_serializer = URLSafeTimedSerializer(
        app.config['SECRET_KEY'])

    password_reset_url = url_for(
        'reset_with_token',
        token=password_reset_serializer.dumps(
            email, salt='password-reset-salt'),
        _external=True)

    msg = Message(subject,
                  recipients=[email])

    msg.html = render_template(
        'email_password_reset.html',
        password_reset_url=password_reset_url)

    mail.send(msg)



# Checks whether the current user has confirmed their email. If not, displays a message.
def email_not_confirmed(user):
    if user.is_authenticated and not user.emailvalidated:
        flash("""Your email has not been confirmed.
         A confirmation email can be resent from the Account page. 
        Password recovery is not possible without a confirmed email and you may lose access to your account.""", "danger")
