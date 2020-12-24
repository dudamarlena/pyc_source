# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/config/middleware.py
# Compiled at: 2007-10-25 12:41:27
"""Pylons middleware initialization"""
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool
from pylons import config
from pylons.error import error_template
from pylons.middleware import error_mapper, ErrorDocuments, ErrorHandler, StaticJavascripts
from pylons.wsgiapp import PylonsApp
from gazest.config.environment import load_environment

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
    app = PylonsApp()
    if asbool(global_conf['staging']):
        print '** Starting in staging mode: no robots allowed'
    if asbool(global_conf['site_readonly']):
        print '** Starting in read only mode: no updates allowed'
    if asbool(full_stack):
        import authkit.authenticate
        app = authkit.authenticate.middleware(app, app_conf=app_conf, global_conf=global_conf)
        app = ErrorHandler(app, global_conf, error_template=error_template, **config['pylons.errorware'])
        app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)
    app = RegistryManager(app)
    javascripts_app = StaticJavascripts()
    static_apps = [ StaticURLParser(path) for path in config['pylons.paths']['static_files'] ]
    app = Cascade(static_apps + [javascripts_app, app])
    return app