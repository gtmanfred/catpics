# Import python libraries
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.hash import sha512_crypt
from flask.ext.login import UserMixin
from catpics import db
import config
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(255), unique=True, primary_key=True)
    password = db.Column(db.String(255))
    info = db.Column(JSON)
    def __init__(self, username, password, roles=[]):
        self.username = username
        self.password = sha512_crypt.encrypt(password)
        self.info = {
            'roles': roles
        }

    def generate_auth_token(self):
        s = Serializer(config.SECRET_KEY)
        return s.dumps({ 'username': self.username})

    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['username'])
        return user

    def check_password(self, password):
        return sha512_crypt.verify(password, self.password)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    @classmethod
    def get(cls, username):
        return cls.query.get(username)

    def get_id(self):
        return User.query.get(self.username).username
 
    def __repr__(self):
        return '<User %r>' % (self.username)
