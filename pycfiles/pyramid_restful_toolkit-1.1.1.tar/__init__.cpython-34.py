# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /sources/github/pyramid_restful_toolkit/pyramid_restful_toolkit/__init__.py
# Compiled at: 2014-08-28 06:11:00
# Size of source mod 2**32: 859 bytes
__author__ = 'tarzan'
from datetime import datetime

class ErrorResponse(Exception):

    def __init__(self, code, errors=None, data=None):
        self.code = code
        self.errors = errors or {}
        self.data = data or {}
        self.message = '%d: %s %s' % (code, errors, data)

    def response(self, request):
        request.response.status_code = self.code
        data = {'data': self.data} if self.data else {}
        data['error_code'] = self.code
        data['errors'] = self.errors
        return data


from .tweens import jsonize_uncaught_exception_tween_factory
from .renderer import default_renderer

def includeme(config):
    """
    :type config: pyramid.config.Configurator
    """
    config.add_renderer(None, default_renderer)
    config.add_renderer('json', default_renderer)
    config.include(__name__ + '.error_handlers')