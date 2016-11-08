from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String(100))
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, name, authenticated=False):
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        self.authenticated = authenticated

    def __repr__(self):
        return '<User &r>' % self.username

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
