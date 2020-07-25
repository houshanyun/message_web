import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:
    dbpath = 'sqlite:///'
else:
    dbpath = 'sqlite:////'


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'abcdefg')
app.config['SQLALCHEMY_DATABASE_URI'] = dbpath + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
moment = Moment(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from myapp.models import Nickname
    admin = Nickname.query.get(int(user_id))
    return admin

login_manager.login_view = 'login'

from myapp import views, commands, errors

