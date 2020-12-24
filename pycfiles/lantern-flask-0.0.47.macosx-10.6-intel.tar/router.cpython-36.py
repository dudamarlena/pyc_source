# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jceciliano/coding/Lantern/lantern-flask/.virtualenv/lib/python3.6/site-packages/lantern_flask/flask/router.py
# Compiled at: 2018-11-30 11:45:11
# Size of source mod 2**32: 1116 bytes
import logging
from flask import Blueprint
from flask_cors import CORS
from lantern_flask import api
log = logging.getLogger(__name__)

class Router(object):
    __doc__ = ' Routing for flask and blueprint\n    '
    api = None
    endpoints = []

    def __init__(self, path, description='', use_cors=True):
        self.api = api
        self.path = path
        self.description = description
        self.use_cors = use_cors

    def init(self, flask_app):
        """ Initialize the app, called from entry point """
        blueprint = Blueprint('api', __name__)
        self.api.init_app(blueprint)
        self._init_endpoints()
        if self.use_cors:
            CORS(flask_app)
        flask_app.register_blueprint(blueprint)

    def register(self, fn):
        """ Add a new function for registering that endpoint
        """
        self.endpoints.append(fn)

    def _get_namespace(self):
        return self.api.namespace((self.path), description=(self.description))

    def _init_endpoints(self):
        ns = self._get_namespace()
        for fn in self.endpoints:
            fn(ns=ns, api=(self.api))