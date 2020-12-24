# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/charles/code/flask-peewee/example/app.py
# Compiled at: 2018-01-17 11:50:43
from flask import Flask
from flask_peewee.db import Database
app = Flask(__name__)
app.config.from_object('config.Configuration')
db = Database(app)

def create_tables():
    User.create_table()
    Relationship.create_table()
    Message.create_table()
    Note.create_table()


@app.template_filter('is_following')
def is_following(from_user, to_user):
    return from_user.is_following(to_user)