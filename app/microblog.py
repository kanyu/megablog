from app import appp, db
from app.models import User, Post

@appp.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'Post': Post
            }