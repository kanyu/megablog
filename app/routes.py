from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User
from app.forms import LoginForm, RegistrationForm
from app import myApp, db

print("==================BLOG START=====================")
import config
import os
print(config.basedir)
print(os.environ.get('DATABASE_URL'))
print(os.path.join(config.basedir, 'app\\app.db'))
print("=================================================")


@myApp.route('/')  # this route alway first
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
