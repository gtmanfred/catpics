from __future__ import print_function
import requests
from passlib.hash import sha512_crypt

import cloud
from catpics import db
from catpics.cloud.cloudfiles import Container
from catpics.models import User
from catpics.api.auth import require_role

from flask.views import MethodView
from flask.ext.login import login_user, logout_user, login_required
from flask import render_template, request, url_for, redirect, abort, g, session
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webm', 'gifv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Index(MethodView):
    def get(self):
        return render_template('index.html')


class Random(MethodView):
    def get(self):
        return render_template('random.html')


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
        return redirect(n or '/')


class Logout(MethodView):
    decorators = [login_required]
    def get(self):
        logout_user()
        n = request.args.get('next')
        return redirect(n or '/')


class Upload(MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('upload.html')

    def post(self):
        f = None
        link = request.form.get('link')
        if 'file' in request.files:
            f = request.files['file'].stream
            filename = request.files['file'].filename
        elif isinstance(link, unicode) and (
                link.startswith('http://') or
                link.startswith('https://')):
            if link.endswith('.gifv'):
                link = link.replace('.gifv', '.webm')
            f = requests.get(link, stream=True)
            f.read = lambda: f.content
            filename = link.split('/')[-1]

        if f and allowed_file(filename):
            filename = secure_filename(filename)
            api = Container(cloud, cloud.container)
            api.create_container()
            api.enable_cdn()
            api.get_cdn()
            ret = api.add_file(filename, f)
            with open('catpics.log', 'a') as catlog:
                print('{ret} -> {username} -> {filename}'.format(ret=ret, username=g.user.username, filename=filename), file=catlog)
        return render_template('upload.html')


class Admin(MethodView):
    decorators = [login_required, require_role('admin')]
    def get(self):
        return render_template('admin.html')


class Password(MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('password.html')

    def post(self):
        if request.form['password1'] != request.form['password2']:
            return redirect('/passwords', 501)

        user = User.query.filter_by(username=g.user.username).first()
        user.password = sha512_crypt.encrypt(request.form['password1'])
        db.session.commit()
        return redirect('/')


class Users(MethodView):
    decorators = [login_required, require_role('admin')]
    def post(self):
        json_dict = {
            'username': request.form['username'],
            'password': request.form['password'],
            'roles': ['users'],
        }

        if request.form.get('admin', False):
            json_dict['roles'].append('admin')

        if 'username' not in json_dict or 'password' not in json_dict:
            abort(400)

        user = User(**json_dict)
        db.session.add(user)
        db.session.commit()
        return redirect('/admin')
