from flask.ext.login import login_user, logout_user, login_required
from flask import request, flash, url_for, redirect, render_template
from catpics import app, db, User

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))
 

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Username is invalid' , 'error')
        return redirect(url_for('login'))
    elif not user.check_password(password):
        flash('Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 


@app.route('/index')
@login_required
def index():
    return render_template('index.html')
