import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-i-cant-tell'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db' or (
            'sqlite:///' + os.path.join(basedir,'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

