from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fridge_name = db.Column(db.String(100), unique=True)
    secret_key = db.Column(db.String(100), unique=True)
    team = db.Column(db.String(100), unique=False)