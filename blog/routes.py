"""Application routes."""
from datetime import datetime

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from .models import User, Post, db
from .forms import UserLoginForm, UserRegistrationForm, UserModificationForm, PostForm
from . import bcrypt
from .file_stuffs import save_picture


@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
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

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UserModificationForm()
    if form.validate_on_submit():
        if form.profile_image.data:
            profile_image_file = save_picture(form.profile_image.data)
            current_user.profile_image = profile_image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.write_date = datetime.utcnow()
        db.session.commit()
        flash('Account updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    account_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', title='Account', account_image=account_image, form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('post_create.html', form=form, title='New Post', legend='New Post')

@app.route('/portfolio')
def about():
    return render_template('portfolio.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')