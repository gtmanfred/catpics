import sys

from itsdangerous import (TimedJSONWebSignatureSerializer
                                  as Serializer, BadSignature, SignatureExpired)
from flask import Flask, Response, jsonify, g, session, request
from flask.ext.login import LoginManager, UserMixin, login_required, current_user
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@app.before_request
def before_request():
    g.user = current_user

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(128))
    

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def check_password(self, password):
        return self.password == password

    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({ 'username': self.username})

    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['username'])
        return user

    @classmethod
    def get(cls, username):
        return cls.query.get(username)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('X-Auth-Token')
    if token:
        return User.verify_auth_token(token)
    else:
        username = request.headers.get('X-Username')
        password = request.headers.get('X-Password')
        user = User.query.get(username)
        if user.check_password(password):
            return user
    return None

@app.route("/api/tokens", methods=["POST"])
@login_required
def get_api_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token.decode('utf-8')})


@app.route("/",methods=["GET"])
def index():
    return Response(response="Hello World!",status=200)


@app.route("/protected/",methods=["GET", "POST"])
@login_required
def protected():
    return Response(response="Hello Protected World!", status=200)


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/catpics"
    db.create_all()
    app.run(port=5000, debug=True)
