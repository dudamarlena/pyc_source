# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/daniel/workarea/preset/Flask-AppBuilder/flask_appbuilder/tests/config_api.py
# Compiled at: 2020-03-31 08:10:13
# Size of source mod 2**32: 352 bytes
import os
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = 'thisismyscretkey'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
FAB_API_SWAGGER_UI = True
FAB_ROLES = {'ReadOnly': [
              [
               '.*', 'can_get'],
              [
               '.*', 'can_info'],
              [
               '.*', 'can_list'],
              [
               '.*', 'can_show']]}