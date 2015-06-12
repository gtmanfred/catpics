import sys

from itsdangerous import (TimedJSONWebSignatureSerializer
                                  as Serializer, BadSignature, SignatureExpired)
from flask import Flask, Response, jsonify, g, session, request
from flask.ext.login import LoginManager, UserMixin, login_required, current_user
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

login_manager = LoginManager()
login_manager.init_app(app)

@app.before_request
def before_request():
    g.user = current_user

class User(UserMixin):
    # proxy for a database of users
    user_database = {"JohnDoe": ("JohnDoe", "John"),
               "JaneDoe": ("JaneDoe", "Jane")}

    def __init__(self, username, password):
        self.id = username
        self.password = password

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.get(data['id'])
        return user

    @classmethod
    def get(cls,id):
        return cls.user_database.get(id)


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('X-Auth-Token')
    if token is None:
        token = request.args.get('token')

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
    return None

@auth.verify_password
def verify_token(username, password):
    token = request.headers.get('X-Auth-Token')
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


@app.route("/api/tokens", methods=["POST"])
@auth.login_required
def get_api_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token.decode('utf-8')})


@app.route("/",methods=["GET"])
def index():
    return Response(response="Hello World!",status=200)


@app.route("/protected/",methods=["GET", "POST"])
@auth.login_required
def protected():
    return Response(response="Hello Protected World!", status=200)


if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(port=5000,debug=True)
