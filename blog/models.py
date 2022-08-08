"""Data models."""
from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    # __tablename__ = 'blog.users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(60), index=True, nullable=False)
    profile_image = db.Column(db.String(40), nullable=False, default='default.jpeg')
    admin = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    write_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Post(db.Model):
    # __tablename__ = 'blog.posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    write_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Post {self.title}, {self.create_date}>"
        