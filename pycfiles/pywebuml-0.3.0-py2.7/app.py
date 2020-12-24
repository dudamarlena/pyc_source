# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pywebuml\app.py
# Compiled at: 2011-02-20 14:03:24
"""
The main module that is used by the web application and by the command that
initilize the database.
"""
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
from pywebuml.settings import DATABASE_URL, DEBUG, DEBUG_DATABASE
app = Flask('pywebuml')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_ECHO'] = DEBUG_DATABASE
app.debug = DEBUG
db = SQLAlchemy(app)