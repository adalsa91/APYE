from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(100))

    def __init__(self, username, email, name):
        self.username = username
        self.email = email
        self.name = name

    def __repr__(self):
        return '<User &r>' % self.username
