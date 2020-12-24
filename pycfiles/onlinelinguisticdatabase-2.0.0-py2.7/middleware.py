# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/config/middleware.py
# Compiled at: 2016-09-19 13:27:02
"""Pylons middleware initialization.

.. module:: middleware
   :synopsis: middleware initialization.

"""
from beaker.middleware import SessionMiddleware
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool
from pylons.middleware import ErrorHandler, StatusCodeRedirect
from pylons.wsgiapp import PylonsApp
from routes.middleware import RoutesMiddleware
from onlinelinguisticdatabase.config.environment import load_environment
import logging, pprint
log = logging.getLogger(__name__)

class HTML2JSONContentType(object):
    """Middleware transforms ``Content-Type: text/html`` headers to ``Content-Type: application/json``.

    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        def custom_start_response(status, headers, exc_info=None):
            new_headers = dict(headers)
            if dict(headers).get('Content-Type') == 'text/html; charset=utf-8':
                new_headers['Content-Type'] = 'application/json'
            try:
                origin = environ.get('HTTP_ORIGIN')
            except Exception as e:
                origin = 'http://dativebeta.lingsync.org'

            if not origin:
                origin = 'http://localhost:9000'
            new_headers['Access-Control-Allow-Origin'] = origin
            new_headers['Access-Control-Allow-Credentials'] = 'true'
            new_headers['Access-Control-Allow-Methods'] = 'GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT, COPY, OPTIONS, SEARCH'
            new_headers['Access-Control-Allow-Headers'] = 'Content-Type, content-type'
            new_headers['Access-Control-Expose-Headers'] = 'Access-Control-Allow-Origin, Access-Control-Allow-Credentials'
            headers = new_headers.items()
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)


def make_app(global_conf, full_stack=False, static_files=True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether this application provides a full WSGI stack (by default,
        meaning it handles its own exceptions and errors). Disable
        full_stack when this application is "managed" by another WSGI
        middleware.

    ``static_files``
        Whether this application serves its own static files; disable
        when another web server is responsible for serving them.

    ``app_conf``
        The application's local configuration. Normally specified in
        the [app:<name>] section of the Paste ini file (where <name>
        defaults to main).

    """
    config = load_environment(global_conf, app_conf)
    app = PylonsApp(config=config)
    app = RoutesMiddleware(app, config['routes.map'], singleton=False)
    app = SessionMiddleware(app, config)
    app = HTML2JSONContentType(app)
    if asbool(full_stack):
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [400, 401, 403, 404, 500])
    app = RegistryManager(app)
    if asbool(static_files):
        static_app = StaticURLParser(config['pylons.paths']['static_files'])
        app = Cascade([static_app, app])
    app.config = config
    return app