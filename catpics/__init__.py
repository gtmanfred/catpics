from flask import Flask, g
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

from catpics.api.models import User
import catpics.api.app

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
    app.register_blueprint(catpics.api.app.create_app())
    app.run()

if __name__ == '__main__':
    run()
