from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from werkzeug.urls import url_parse
from app.models import User
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app import myApp, db

print("==================BLOG START=====================")
import config
from config import Config
import os
print("mail server: ", Config.MAIL_SERVER)
print("mail port: ", Config.MAIL_PORT)
print("basedir :", config.basedir)
print("database URL: ", os.environ.get('DATABASE_URL'))
print("database file: ", os.path.join(config.basedir, 'app\\app.db'))
print("=================================================")

# 'before_request' This decorator from Flask register the decorated function
# to be executed right before every view functions


@myApp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@myApp.route('/')  # this route always first
@myApp.route('/index')
@login_required  # this decorator to protect page which need login
def index():
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
    return render_template('index.html', title='Home', posts=posts)


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
        # create request to redirect
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # redirect to page where user come from
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@myApp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@myApp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@myApp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'},
    ]
    return render_template('user.html', user=user, posts=posts)


@myApp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)  # create form instance from class in forms.py
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
