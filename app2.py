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

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
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
        user = User.get(data['username'])
        return User(user[0], user[1])

    @classmethod
    def get(cls, username):
        return cls.user_database.get(username)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('X-Auth-Token')
    if not token:
        json_dict = request.get_json(force=True)
        if not json_dict:
            abort(401)
        username = json_dict.get('username')
        password = json_dict.get('password')
        user_entry = User.get(username)
        if user_entry is not None:
            user = User(user_entry[0], user_entry[1])
            if user.password == password:
                return user
    else:
        return User.verify_auth_token(token)

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
