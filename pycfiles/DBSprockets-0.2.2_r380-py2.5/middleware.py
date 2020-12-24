# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/dbmechanic/frameworks/tg2/test/TG2TestApp/tg2testapp/config/middleware.py
# Compiled at: 2008-06-30 11:43:44
"""Pylons middleware initialization"""
from beaker.middleware import SessionMiddleware, CacheMiddleware
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool
from paste import httpexceptions
from pylons import config
from pylons.middleware import error_mapper, ErrorDocuments, ErrorHandler, StaticJavascripts, StatusCodeRedirect
from pylons.wsgiapp import PylonsApp
from routes.middleware import RoutesMiddleware
from tw.core.middleware import TGWidgetsMiddleware
from tw.mods.pylonshf import PylonsHostFramework
from tg2testapp.config.environment import load_environment

def make_app(global_conf, full_stack=True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether or not this application provides a full WSGI stack (by
        default, meaning it handles its own exceptions and errors).
        Disable full_stack when this application is "managed" by
        another WSGI middleware.

    ``app_conf``
        The application's local configuration. Normally specified in the
        [app:<name>] section of the Paste ini file (where <name>
        defaults to main).
    """
    load_environment(global_conf, app_conf)
    from tg2testapp.controllers.root import RootController
    app = PylonsApp()
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    host_framework = PylonsHostFramework(default_view='genshi')
    app = TGWidgetsMiddleware(app, host_framework)
    if asbool(full_stack):
        app = ErrorHandler(app, global_conf, **config['pylons.errorware'])
        if asbool(config['debug']):
            app = StatusCodeRedirect(app)
        else:
            app = StatusCodeRedirect(app, [400, 401, 403, 404, 500])
    app = RegistryManager(app)
    javascripts_app = StaticJavascripts()
    static_app = StaticURLParser(config['pylons.paths']['static_files'])
    app = Cascade([static_app, javascripts_app, app])
    return app