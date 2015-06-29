from flask import Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from catpics import app


def create_app():
    app = Blueprint('frontend', __name__, url_prefix='/api')

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
