from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

appp = Flask(__name__)  #  __name__ : name of package
appp.config.from_object(Config)
db = SQLAlchemy(appp)
migrate = Migrate(appp, db)
login = LoginManager(appp)
login.login_view = 'login'

from app import routes, models

