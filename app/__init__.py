from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler

myApp = Flask(__name__)
myApp.config.from_object(Config)
db = SQLAlchemy(myApp)
migrate = Migrate(myApp, db)
login = LoginManager(myApp)
login.login_view = 'login'

if not myApp.debug:
    if myApp.config['MAIL_SERVER']:
        auth = None
        if myApp.config['MAIL_USERNAME'] or myApp.config['MAIL_PASSWORD']:
            auth = (myApp.config['MAIL_USERNAME'], myApp.config['MAIL_PASSWORD'])
        secure = None
        if myApp.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(myApp.config['MAIL_SERVER'], myApp.config['MAIL_PORT']),
            fromaddr='no-reply@' + myApp.config['MAIL_SERVER'],
            toaddrs=myApp.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        myApp.logger.addHandler(mail_handler)

from app import routes, models, errors