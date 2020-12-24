# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/baseui/__init__.py
# Compiled at: 2017-11-09 12:25:16
# Size of source mod 2**32: 547 bytes
from flask import Blueprint

class BaseUI(object):
    __doc__ = 'Attaches a base UI blueprint to an application.'

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Creates and registers the base UI blueprint."""
        blueprint = Blueprint('baseui',
          __name__,
          template_folder='templates',
          static_folder='static',
          static_url_path=(app.static_url_path + '/base'))
        app.register_blueprint(blueprint)