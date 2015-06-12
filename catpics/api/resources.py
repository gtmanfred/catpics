from flask.ext.login import login_user, logout_user, login_required
from flask import request, flash, url_for, redirect, render_template, g, jsonify, abort
from catpics import app, db, User, auth

@app.route('/api/token', methods=['POST'])
def get_api_token():
    if request.method == 'GET':
        abort(401)
    json_dict = request.get_json(force=True)
    username = json_dict.get('username')
    password = json_dict.get('password')
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(401, "User doesn't exist")
    elif not user.check_password(password):
        abort(401, "Invalid Password")
    login_user(user)

    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@app.route('/index')
@auth.login_required
def index():
    return render_template('index.html')
