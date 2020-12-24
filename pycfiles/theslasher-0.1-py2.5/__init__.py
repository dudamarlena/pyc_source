# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/theslasher/__init__.py
# Compiled at: 2010-01-11 17:48:16
"""
request dispatcher
"""
from webob import Request, exc

class TheSlasher(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        if request.path_info.endswith('/') and request.path_info != '/':
            location = request.path_info.rstrip('/')
            return exc.HTTPMovedPermanently(location=location)(environ, start_response)
        return self.app(environ, start_response)