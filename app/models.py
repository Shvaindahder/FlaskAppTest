from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY


class UserAccount(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Hieroglyph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hieroglyph = db.Column(db.String(1), unique=True)
    onyomi = db.Column(ARRAY(db.String(10)))
    kunyomi = db.Column(ARRAY(db.String(10)))
    translation = db.Column(ARRAY(db.String(20)))

    def __repr__(self):
        return '<Hieroglyph {}>'.format(self.hieroglyph)


@login.user_loader
def load_user(id):
    return UserAccount.query.get(int(id))