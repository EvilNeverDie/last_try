from flask_app import db, login_manager
from flask_login import UserMixin
from flask_migrate import Migrate
from flask_script import Manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    urls = db.relationship('Url', backref='user-hyuser', lazy='dynamic')
    user_selector = db.Column(db.String(50))


class Url(db.Model):
    id = db.Column(db.Integer(),  primary_key=True)
    url = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hash = db.Column(db.String(100))
    flag = db.Column(db.Integer())



db.create_all()