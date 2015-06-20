from flask import Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from catpics import app

db = SQLAlchemy(app)
api = Blueprint('api', __name__, url_prefix='/api')

from catpics.api.models import User
