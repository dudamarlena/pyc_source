# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/flaskapp/base/app.py
# Compiled at: 2019-07-24 05:34:04
# Size of source mod 2**32: 1452 bytes
import hashlib
from flask import Flask, render_template, request, session
from database import db_session
from models import User
from utils import get_hash
app = Flask(__name__)
app.secret_key = '{SECRET_KEY}'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        username = request.form['username']
        password = get_hash(request.form['password'], app.secret_key)
        if User.query.filter(User.name == username).first():
            return render_template('error.html')
        u = User(username, password)
        db_session.add(u)
        db_session.commit()
        return render_template('login.html')
    return render_template('sign.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = get_hash(request.form['password'], app.secret_key)
        if User.query.filter(User.name == username and User.password == password).first():
            session['logged_in'] = True
            session['username'] = username
            return render_template('index.html')
        return 'Fail'
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)