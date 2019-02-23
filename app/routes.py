from flask import render_template
from app import myApp


@myApp.route('/')
@myApp.route('/index')
def index():
    user = {'username': 'Kan'}
    posts = [
        {
            'author': {'username': 'Thor'},
            'body': 'Beautiful Thailand!'
        },
        {
            'author': {'username': 'Nano'},
            'body': 'The Alita movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)