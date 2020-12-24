# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/__init__.py
# Compiled at: 2017-11-20 09:04:05
# Size of source mod 2**32: 1669 bytes
import logging
from flask import jsonify
from werkzeug.exceptions import default_exceptions
__author__ = 'stas'
__version__ = '0.2.1'
from flask_restframework.serializer import BaseSerializer
from flask_restframework.exceptions import BaseException

def common_exception_handler(e):
    logging.getLogger('flask_restframework').getChild('exception_handler').exception('Getted common exception: %s', e, extra={'meta': e})
    resp = jsonify({'error': e.__class__.__name__, 
     'code': 500, 
     'description': str(e)})
    resp.status_code = 500
    return resp


def http_exception_handler(e):
    logging.getLogger('flask_restframework').getChild('exception_handler').error('Getted http exception: %s', e, exc_info=True, extra={'meta': e})
    resp = jsonify({'error': e.name, 
     'code': e.code, 
     'description': e.description})
    resp.status_code = e.code
    return resp


def base_exception_handler(e):
    data = getattr(e, 'data')
    status = e.status
    out = jsonify(data or {})
    out.status_code = status
    return out


class RestFramework(object):

    def __init__(self, app=None):
        self.init_app(app)

    def init_app(self, app):
        self.app = app
        return self

    def init_errorhandlers(self):
        self.app.errorhandler(Exception)(common_exception_handler)
        self.app.errorhandler(BaseException)(base_exception_handler)
        for code, ex in default_exceptions.items():
            self.app.errorhandler(code)(http_exception_handler)

        return self