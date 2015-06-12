from functools import wraps
from flask import g, abort

def require_role(role):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if role not in g.user.info.get('roles', []):
                return abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
