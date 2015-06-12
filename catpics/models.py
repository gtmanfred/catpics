# Import python libraries
from passlib.hash import sha512_crypt

from catpics import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    pw_hash = db.Column(db.String(255))
    activated = db.Column(db.Boolean(True))
    confirmed_at = db.Column(db.DateTime())
    def __init__(self, username, password):
        self.username = username
        self.pw_hash = sha512_crypt.encrypt(password)
        self.activated = True

    def check_password(self, password):
        return sha512_crypt.verify(password, self.pw_hash)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return self.activated
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)


