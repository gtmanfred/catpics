# Import python libraries
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.hash import sha512_crypt

from catpics import db, app, UserMixin

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

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

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


