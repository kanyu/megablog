from flask import Flask
from config import Config

myApp = Flask(__name__)
myApp.config.from_object(Config)

from app import routes