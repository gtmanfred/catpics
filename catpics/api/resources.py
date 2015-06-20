from flask.ext.login import login_user, logout_user, login_required
from flask import request, jsonify, abort
from catpics import app, db, User, g, cloud
from catpics.api.auth import require_role

from catpics.cloud.cloudfiles import Container


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

@app.route('/upload/<upload_file>', methods=["POST"])
def upload_file(upload_file):
    print(request.method)
    print(request.files)
    print(request.stream.__dict__)
    api = Container(app.cloud, 'epel')
    #return jsonify({"files": api.list_files})
    api.create_container('epel')
    api.add_file(upload_file, request.stream)
    return jsonify({"files": api.list_files()})
