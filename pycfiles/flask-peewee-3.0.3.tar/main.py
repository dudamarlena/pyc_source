# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/charles/code/flask-peewee/example/main.py
# Compiled at: 2018-01-17 11:50:43
from app import app, db
from auth import *
from admin import admin
from api import api
from models import *
from views import *
admin.setup()
api.setup()
if __name__ == '__main__':
    app.run()