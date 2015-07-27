from flask import Blueprint

from catpics.client import resources


def create_app():
    app = Blueprint('frontend', __name__)
    app.add_url_rule('/', view_func=resources.Index.as_view('index'))
    app.add_url_rule('/random', view_func=resources.Random.as_view('random'))
    app.add_url_rule('/login', view_func=resources.Login.as_view('login'))
    app.add_url_rule('/logout', view_func=resources.Logout.as_view('logout'))
    app.add_url_rule('/upload', view_func=resources.Upload.as_view('upload'))
    return app
