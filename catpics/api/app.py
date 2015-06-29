from flask import Blueprint
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from catpics import app


def create_app():
    app = Blueprint('backend', __name__, url_prefix='/api')
    api = Api(app)

    from catpics.api.resources import (
        APIToken,
        Users,
        RandomImage,
        Image,
    )
    resources = {
        APIToken: '/tokens',
        Users: '/users',
        RandomImage: '/random',
        Image: '/images/<image>',
    }

    for resource, route in resources.items():
        api.add_resource(resource, route)

    return app
