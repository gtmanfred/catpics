from flask.ext.login import login_user, logout_user, login_required
from flask import request, flash, url_for, redirect, render_template, g, jsonify, abort
from catpics import app, db, User, auth
from catpics.api.auth import require_role

@app.route("/api/tokens", methods=["POST"])
@login_required
def get_api_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token.decode('utf-8')})

@app.route("/api/users", methods=["POST"])
@login_required
def create_user():
    json_dict = request.get_json(force=True)
    if 'username' not in json_dict or 'password' not in json_dict:
        abort(400)

    user = User(**json_dict)
    db.session.add(user)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/index')
@login_required
@require_role('admin')
def index():
    ret = {x:y for x, y in g.user.__dict__.items() if not x.startswith('_')}
    return jsonify(ret)

@app.route('/random')
def random_image():
    return jsonify({"status": "in progress"})
