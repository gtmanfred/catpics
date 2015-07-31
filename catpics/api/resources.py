import os
import random
import requests

from flask.ext.login import login_user, logout_user, login_required
from flask.ext.restful import Resource
from flask import request, jsonify, abort, g
from werkzeug import secure_filename

import cloud
from catpics import db
from catpics.models import User
from catpics.api.auth import require_role

from catpics.cloud.cloudfiles import Container

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'webm', 'gifv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class APIToken(Resource):
    decorators = [login_required]
    def post(self):
        token = g.user.generate_auth_token()
        return jsonify({"token": token.decode('utf-8')})


class Users(Resource):
    decorators = [login_required, require_role('admin')]
    def post(self):
        json_dict = request.get_json(force=True)
        if 'username' not in json_dict or 'password' not in json_dict:
            abort(400)

        user = User(**json_dict)
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": "success"})


class RandomImage(Resource):
    def get(self):
        api = Container(cloud, cloud.container)
        api.get_cdn()
        image = random.choice(api.list_files())
        ret = {}
        if image.endswith('.gifv') or image.endswith('.webm'):
            ret['type'] = 'video'
            ret['suffix'] = 'webm'
        else:
            ret['type'] = 'image'
            ret['suffix'] = image.split('.')[-1]
        link = api.links['X-Cdn-Ssl-Uri']
        ret['image'] = os.path.join(link, image)
        return jsonify(ret)


class Image(Resource):
    decorators = [login_required, require_role('user')]
    def get(self, image):
        api = Container(cloud, cloud.container)
        api.create_container()
        api.enable_cdn()
        api.get_cdn()
        return jsonify({"image": os.path.join(api.links['X-Cdn-Ssl-Uri'], image)})

    def post(self, image):
        f = None
        link = request.json.get('link')
        if 'file' in request.files:
            filename = image
            f = request.files['file'].stream
        elif isinstance(link, str) and (
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
            api.add_file(filename, f)
        return jsonify({"success": filename})

    def delete(self, image):
        api = Container(cloud, cloud.container)
        api.create_container()
        api.enable_cdn()
        api.get_cdn()
        api.delete_file(image)
        return jsonify({"success": image})
