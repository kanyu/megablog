from app import myApp, db
from app.models import User, Post


@myApp.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}