
from flask import Flask, g
from flask.ext.login import current_user, LoginManager, UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
 
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

from catpics.api.models import User
from catpics.api import resources

@login_manager.request_loader
def load_user(request):
    token = request.headers.get('X-Auth-Token')
    if token:
        return User.verify_auth_token(token)
    else:
        username = request.headers.get('X-Username')
        password = request.headers.get('X-Password')
        if username is None:
            return None
        user = User.query.get(username)
        if user is not None and user.check_password(password):
            return user
    return None

@app.before_request
def before_request():
    g.user = current_user

def run():
    db.create_all()
    app.run()

if __name__ == '__main__':
    run()
