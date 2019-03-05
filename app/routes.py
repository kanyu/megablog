from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from werkzeug.urls import url_parse
from app.models import User, Post
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
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
print("page config:", myApp.config['POSTS_PER_PAGE'])
print("=================================================")

# 'before_request' This decorator from Flask register the decorated function
# to be executed right before every view functions


@myApp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@myApp.route('/', methods=['GET', 'POST'])  # this route always first
@myApp.route('/index', methods=['GET', 'POST'])
@login_required  # this decorator to protect page which need login
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, myApp.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',
                           title='Home',
                           form=form,
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url
                           )


@myApp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, myApp.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',
                           title='Explore',
                           posts=posts.items,
                           form=False,
                           next_url=next_url,
                           prev_url=prev_url
                           )


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
    return render_template('login.html',
                           title='Sign In',
                           form=form
                           )


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
    return render_template('register.html',
                           title='Register',
                           form=form
                           )


@myApp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, myApp.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html',
                           user=user,
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url
                           )


@myApp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)  # render form from from.py
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',
                           title='Edit Profile',
                           form=form
                           )


@myApp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username = username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@myApp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


