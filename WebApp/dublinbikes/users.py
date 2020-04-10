from dublinbikes import login_manager, mail, app
from flask_login import UserMixin
from flask_mail import Message
from flask import render_template, url_for, flash
from itsdangerous import URLSafeTimedSerializer
import mysql.connector
import json

def get_password(email):
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('get_password', [email, ])

        results = mycursor.stored_results()

    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)


    for result in results:
        password = result.fetchall()[0][0]

    mycursor.close()
    mydb.close()

    return password




def add_user(email, password):
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('add_user', (email, password, ))
        mydb.commit()

        print(mycursor.rowcount)
    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

    mycursor.close()
    mydb.close()
    


def add_favourite_station(stations, user_id):
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('add_station_to_user', (stations, user_id, ))
        mydb.commit()

        print(mycursor.rowcount)
    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)

    mycursor.close()
    mydb.close()
    

# def get_password(email):
#     pass

def get_favourite_stations(id):
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

        mycursor = mydb.cursor()

        # called mysql stored procedure giving email as an argument
        mycursor.callproc('get_fav_stations_by_id', [id, ])

        results = mycursor.stored_results()

    except mysql.connector.Error as err:

        print("SOMETHING WENT WRONG:", err)


    for result in results:
        stations = result.fetchall()[0][0]

    mycursor.close()
    mydb.close()

    return stations


def check_email(email):
    try:
        # Connect to the RDS database
        mydb = mysql.connector.connect(
            host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
            user="admin",
            passwd="fmRdzKkP6mTtwEEsCByh",
            database="dublinbikes"
        )

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


@login_manager.user_loader
def load_user(email):
    if(check_email(email)):
        return User(email)
    else:
        return None


class User(UserMixin):
    def __init__(self, email):
        try:
            # Connect to the RDS database
            mydb = mysql.connector.connect(
                host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
                user="admin",
                passwd="fmRdzKkP6mTtwEEsCByh",
                database="dublinbikes"
            )

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
            mydb = mysql.connector.connect(
                host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
                user="admin",
                passwd="fmRdzKkP6mTtwEEsCByh",
                database="dublinbikes"
            )

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
            mydb = mysql.connector.connect(
                host="dublin-bikes.cy2mnwcfkfbs.eu-west-1.rds.amazonaws.com",
                user="admin",
                passwd="fmRdzKkP6mTtwEEsCByh",
                database="dublinbikes"
            )

            mycursor = mydb.cursor()
            print("feattuer:", feature)
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
                mycursor.callproc('update_stations', [self.email, json.dumps(self.stations)])

            elif feature == "remove_station":
                if data in self.stations:
                    self.stations.remove(data)
                mycursor.callproc('update_stations', [self.email, json.dumps(self.stations)])

                
            mydb.commit()
        except mysql.connector.Error as err:

            print("SOMETHING WENT WRONG:", err)

        mycursor.close()
        mydb.close()

    def __repr__(self):
        return f"{self.email}, {self.password}, {self.stations}"


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




def email_not_confirmed(user):
    if user.is_authenticated and not user.emailvalidated:
        flash("""Your email has not been confirmed.
         A confirmation email can be resent from the Account page. 
        Password recovery is not possible without a confirmed email and you may lose access to your account.""", "danger")
