# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattpease/DevTools/Workspaces/flask-spawn/flaskspawn/cookiecutters/small/{{cookiecutter.repo_name}}/config.py
# Compiled at: 2015-07-07 17:30:27
import os

class Config(object):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False