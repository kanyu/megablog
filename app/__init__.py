from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

myApp = Flask(__name__)
myApp.config.from_object(Config)
db = SQLAlchemy(myApp)
migrate = Migrate(myApp, db)

from app import routes