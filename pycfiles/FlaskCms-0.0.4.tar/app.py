# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyle/fcms/flask-cms/flask_cms/app.py
# Compiled at: 2016-01-26 17:48:15
"""
    app.py
    ~~~~~~

    app initalization
"""
from flask_xxl.main import AppFactory
from settings import DevelopmentConfig
app = AppFactory(DevelopmentConfig).get_app(__name__)