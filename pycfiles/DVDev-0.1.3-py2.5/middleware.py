# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/config/middleware.py
# Compiled at: 2009-04-17 21:14:57
"""Pylons middleware initialization"""
from beaker.middleware import CacheMiddleware, SessionMiddleware
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool
from pylons import config
from pylons.middleware import ErrorHandler, StatusCodeRedirect
from pylons.wsgiapp import PylonsApp
from routes.middleware import RoutesMiddleware
from dvdev.config.environment import load_environment
import os
from repoze.who.config import make_middleware_with_config as make_who_with_config
from repoze.who.middleware import PluggableAuthenticationMiddleware
from repoze.who.interfaces import IIdentifier
from repoze.who.interfaces import IChallenger
from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
from repoze.who.plugins.openid import OpenIdIdentificationPlugin
from repoze.who.classifiers import default_request_classifier
from repoze.who.classifiers import default_challenge_decider

def make_app(global_conf, full_stack=True, static_files=True, **app_conf):
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
    load_environment(global_conf, app_conf)
    app = PylonsApp()
    app = RoutesMiddleware(app, config['routes.map'])
    app = SessionMiddleware(app, config)
    app = CacheMiddleware(app, config)
    auth_tkt = AuthTktCookiePlugin(')h,&xCWlS}+u:<yD]BJV', 'auth_tkt')
    openid = OpenIdIdentificationPlugin('file', openid_field='openid', error_field='error', session_name='beaker.session', login_form_url='/login_form', login_handler_path='/do_login', logout_handler_path='/logout', store_file_path=os.path.join(config['reporoot'], 'sstore'), logged_in_url='/success', logged_out_url='logout_success', came_from_field='came_from', rememberer_name='auth_tkt', sql_associations_table='', sql_nonces_table='', sql_connstring='')
    identifiers = [
     (
      'openid', openid), ('auth_tkt', auth_tkt)]
    authenticators = [('openid', openid)]
    challengers = [('openid', openid)]
    mdproviders = []
    log_stream = None
    if config.get('WHO_LOG'):
        log_stream = sys.stdout
    app = PluggableAuthenticationMiddleware(app, identifiers, authenticators, challengers, mdproviders, default_request_classifier, default_challenge_decider, log_stream=log_stream, log_level=app_conf['who.log_level'])
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
    return app