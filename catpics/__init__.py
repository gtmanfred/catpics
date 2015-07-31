from flask import Flask, g, session
from flask.ext.login import current_user, LoginManager, UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import cloud

app = Flask(__name__)
 
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

from catpics.models import User
import catpics.api.app
import catpics.client.app


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@login_manager.request_loader
def load_request(request):
    token = request.headers.get('X-Auth-Token')
    if token:
        return User.verify_auth_token(token)
    elif request.environ.get('PATH_INFO') == '/api/tokens':
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None:
            return None
        user = User.query.get(username)
        if user is not None and user.check_password(password):
            return user
    return None


@app.before_request
def before_request():
    g.user = current_user
