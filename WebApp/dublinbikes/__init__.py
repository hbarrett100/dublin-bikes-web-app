from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "7d6adad6c27339d1f158ac6341fefb25"

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)