from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.models import User
from app import myApp
from app.forms import LoginForm

print("==================BLOG START=====================")
import config
import os
print(config.basedir)
print(os.environ.get('DATABASE_URL'))
print(os.path.join(config.basedir, 'app\\app.db'))
print("=================================================")
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


@myApp.route('/login', methods=['GET', 'POST'])
def login():
    # check if the user is already logged in return to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # fetch user from DB by form input
        user = User.query.filter_by(username=form.username.data).first()
        # if None user or wrong password return warning 'Invalid username or password'
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # if not wrong and exist log user in
        login_user(user, remember=form.remember_me.data)
        # redirect to page where user come from
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@myApp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
