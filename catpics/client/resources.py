import requests

import cloud
from catpics.cloud.cloudfiles import Container
from catpics.models import User

from flask.views import MethodView
from flask.ext.login import login_user, logout_user, login_required
from flask import render_template, request, url_for, redirect, abort, g, session
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class Index(MethodView):
    def get(self):
        return render_template('index.html')


class Login(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.get(username)
        if user is not None and user.check_password(password):
            login_user(user)
        n = request.args.get('next')
        return redirect('/upload')

class Logout(MethodView):
    decorators = [login_required]
    def get(self):
        logout_user()
        return redirect('/login')


class Upload(MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('upload.html')

    def post(self):
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            api = Container(cloud, cloud.container)
            api.create_container()
            api.enable_cdn()
            api.get_cdn()
            api.add_file(f.filename, f.stream)
        return render_template('upload.html')
