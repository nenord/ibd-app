from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Rest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    alias = db.Column(db.String(64))
    url = db.Column(db.String(240))
    categories = db.Column(db.String(100))
    city = db.Column(db.String(32))
    address = db.Column(db.String(64))
    postal_code = db.Column(db.String(16))
    country = db.Column(db.String(24))
    rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True)
    posts = db.relationship('Post', backref='restaurant', lazy='dynamic')

    def __repr__(self):
        return '<Rest {}>'.format(self.alias)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rest_id = db.Column(db.Integer, db.ForeignKey('rest.id'))


    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Counters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    count = db.Column(db.Integer)

    def __repr__(self):
        return '<Count {}>'.format(self.count)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
