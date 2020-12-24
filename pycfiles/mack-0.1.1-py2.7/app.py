# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mack/project/app.py
# Compiled at: 2017-08-11 19:13:57
from flask import render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os
app = Flask(__name__)
app.secret_key = os.urandom(100)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
Bootstrap(app)
db = SQLAlchemy(app)
app.secret_key = os.urandom(64)

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50), unique=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return ('<User {0}>').format(self.username)


@app.before_first_request
def setup():
    db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    return (render_template('404.html'), 404)


@app.route('/')
def index():
    return render_template('index.html', title='homepage')


if __name__ == '__main__':
    app.run()