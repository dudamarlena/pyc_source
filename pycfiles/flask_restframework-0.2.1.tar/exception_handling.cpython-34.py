# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/exception_handling.py
# Compiled at: 2017-07-04 10:12:16
# Size of source mod 2**32: 2098 bytes
"""
This module provides JSON exception handling.
"""
import logging
from flask import jsonify
from flask.app import Flask
from werkzeug.exceptions import default_exceptions
LOGGER = logging.getLogger('restframework.exceptions')

class ExceptionHandler:
    __doc__ = '\n\n    Usage\n    .. code-block:: python\n\n        ExceptionHandler(app)            .handle_common_exceptions()            .handle_http_exceptions()\n\n    On exception you\'ll get::\n\n        {\n          "code": 500,\n          "description": "exceptions must derive from BaseException",\n          "error": "TypeError"\n        }\n\n    for common exceptions and::\n\n        {\n          "code": 404,\n          "description": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.",\n          "error": "Not Found"\n        }\n\n    for http ones\n\n    '

    def __init__(self, app=None):
        """:type app: Flask"""
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def handle_common_exceptions(self):

        def common_exception_handler(e):
            LOGGER.exception('Getted common exception: %s', e, extra={'meta': e})
            resp = jsonify({'error': e.__class__.__name__, 
             'code': 500, 
             'description': str(e)})
            resp.status_code = 500
            return resp

        self.app.errorhandler(Exception)(common_exception_handler)
        return self

    def handle_http_exceptions(self):

        def handler(e):
            LOGGER.error('Getted http exception: %s', e, exc_info=True, extra={'meta': e})
            resp = jsonify({'error': e.name, 
             'code': e.code, 
             'description': e.description})
            resp.status_code = e.code
            return resp

        for code, ex in default_exceptions.items():
            self.app.errorhandler(code)(handler)

        return self