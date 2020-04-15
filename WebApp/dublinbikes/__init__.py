from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail




app = Flask(__name__)
app.config['SECRET_KEY'] = "7d6adad6c27339d1f158ac6341fefb25"

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'conorlshort@gmail.com'
app.config['MAIL_PASSWORD'] = "rasmhzrmbklbnpas"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'conorlshort@gmail.com'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

