import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

myApp = Flask(__name__)
myApp.config.from_object(Config)
db = SQLAlchemy(myApp)
migrate = Migrate(myApp, db)
login = LoginManager(myApp)
login.login_view = 'login'
mail = Mail(myApp)

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

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    myApp.logger.addHandler(file_handler)
    myApp.logger.setLevel(logging.INFO)
    myApp.logger.info('Microblog startup')


from app import routes, models, errors