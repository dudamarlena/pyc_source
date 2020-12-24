# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tornado_swirl/handlers.py
# Compiled at: 2019-12-17 19:27:20
# Size of source mod 2**32: 962 bytes
"""
Swagger handler utils
"""
from tornado.web import StaticFileHandler, URLSpec
from tornado_swirl.views import SwaggerApiHandler, SwaggerUIHandler
import tornado_swirl.settings as settings
__author__ = 'rduldulao'

def swagger_handlers():
    """Returns the swagger UI handlers

    Returns:
        [(route, handler)] -- list of Tornado URLSpec
    """
    prefix = settings.default_settings.get('swagger_prefix', '/swagger')
    if prefix[(-1)] != '/':
        prefix += '/'
    return [
     URLSpec((prefix + 'spec.html$'), SwaggerUIHandler, (settings.default_settings),
       name=(settings.URL_SWAGGER_API_DOCS)),
     URLSpec((prefix + 'spec$'), SwaggerApiHandler, name=(settings.URL_SWAGGER_API_SPEC)),
     (
      prefix + '(.*\\.(css|png|gif|js))', StaticFileHandler,
      {'path': settings.default_settings.get('static_path')})]