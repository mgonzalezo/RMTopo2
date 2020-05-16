from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c6d7273bf48e8a7ebb88bf139758f13a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
#login view to force to login to access account view
login_manager.login_view = 'login'
#info style to show messages based on bootstrap design
login_manager.login_message_category = 'info'

from webapp import routes
