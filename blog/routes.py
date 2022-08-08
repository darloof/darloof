"""Application routes."""
from datetime import datetime as dt

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for, flash

from .models import User, Post, db
from .forms import UserLoginForm, UserRegistrationForm


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        flash(f'Account {form.username.data} created.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')