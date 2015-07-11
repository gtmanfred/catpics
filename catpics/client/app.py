from flask import Blueprint

from catpics.client import resources


def create_app():
    app = Blueprint('frontend', __name__)
    app.add_url_rule('/', view_func=resources.Index.as_view('index'))
    return app
