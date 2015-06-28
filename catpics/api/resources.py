import os
import random
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.restful import Resource
from flask import request, jsonify, abort, g

import cloud
from catpics import db
from catpics.api.models import User
from catpics.api.auth import require_role

from catpics.cloud.cloudfiles import Container

class APIToken(Resource):
    decorators = [login_required]
    def post(self):
        token = g.user.generate_auth_token()
        return jsonify({"token": token.decode('utf-8')})


class Users(Resource):
    decorators = [login_required]
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
        return jsonify({"image": os.path.join(api.links['X-Cdn-Ssl-Uri'], image)})


class Image(Resource):
    decorators = [login_required, require_role('user')]
    def get(self, image):
        api = Container(cloud, cloud.container)
        api.create_container()
        api.enable_cdn()
        api.get_cdn()
        return jsonify({"image": os.path.join(api.links['X-Cdn-Ssl-Uri'], image)})

    def post(self, image):
        api = Container(cloud, cloud.container)
        api.create_container()
        api.enable_cdn()
        api.get_cdn()
        api.add_file(image, request.stream)
        return jsonify({"files": api.list_files()})

    def delete(self, image):
        api = Container(cloud, cloud.container)
        api.create_container()
        api.enable_cdn()
        api.get_cdn()
        api.delete_file(image)
        return jsonify({"files": api.list_files()})
