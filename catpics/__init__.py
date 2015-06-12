
from flask import Flask, g
from flask.ext.login import current_user, LoginManager, UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api
from datetime import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()
 
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'login'
db = SQLAlchemy(app)

from catpics.api.models import User
from catpics.api import resources

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

def run():
    db.create_all()
    app.run()

if __name__ == '__main__':
    run()
