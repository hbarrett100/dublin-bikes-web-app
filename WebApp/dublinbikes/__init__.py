from flask import Flask
from dublinbikes.config import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail




app = Flask(__name__)
app.config['SECRET_KEY'] = flask_app_config["secret_key"]

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = email_config["username"]
app.config['MAIL_PASSWORD'] = email_config["password"]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEFAULT_SENDER'] = email_config["default_sender"]
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

