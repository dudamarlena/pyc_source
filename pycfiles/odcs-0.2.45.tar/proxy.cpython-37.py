# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/proxy.py
# Compiled at: 2017-08-31 11:17:14
# Size of source mod 2**32: 2327 bytes
"""
Allows ODCS to run behind reverse proxy and to ensure redirects work
with https.

WSGI Middleware!!

Source: http://flask.pocoo.org/snippets/35/ by Peter Hansen
"""

class ReverseProxy(object):
    __doc__ = 'Wrap the application in this middleware and configure the\n    front-end server to add these headers, to let you quietly bind\n    this to a URL other than / and to an HTTP scheme that is\n    different than what is used locally.\n\n    :param app: the WSGI application\n    '

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        server = environ.get('HTTP_X_FORWARDED_HOST', '')
        if server:
            environ['HTTP_HOST'] = server
        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)