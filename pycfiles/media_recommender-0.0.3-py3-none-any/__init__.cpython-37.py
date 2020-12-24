# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\fyp-media-recommender\mediarecommender\recommender\__init__.py
# Compiled at: 2019-04-07 20:08:06
# Size of source mod 2**32: 230 bytes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recommender.db'
db = SQLAlchemy(app)
from mediarecommender.recommender import routes