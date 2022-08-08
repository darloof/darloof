"""Application routes."""
from datetime import datetime

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from .models import User, Post, db
from .forms import UserLoginForm, UserRegistrationForm
from . import bcrypt


@app.route('/')
@app.route('/home')
def home():
    posts = [
        {
            'author': 'darloof',
            'author_id': 1,
            'title': 'this is the first title',
            'content': 'this is the content of first post',
            'date_posted': '2022/08/07',
        },
        {
            'author': 'mahdi',
            'author_id': 2,
            'title': 'this is the seoncd title',
            'content': 'this is the content of seoncd post',
            'date_posted': '2021/08/07',
        },
        {
            'author': 'haniye',
            'author_id': 3,
            'title': 'this is the third title',
            'content': 'this is the content of third post',
            'date_posted': '2020/08/07',
        },
    ] * 4
    return render_template('home.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account {form.username.data} created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/portfolio')
def about():
    return render_template('portfolio.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')