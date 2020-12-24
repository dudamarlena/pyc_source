# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/blobs/wsgiapp.py
# Compiled at: 2008-02-19 12:19:12
"""The blobs WSGI application"""
import os
from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool
from pylons import config
from pylons.error import error_template
from pylons.middleware import error_mapper, ErrorDocuments, ErrorHandler, StaticJavascripts
from pylons.wsgiapp import PylonsApp
from sqlalchemy import engine_from_config
import blobs.helpers
from blobs.routing import make_map
import blobs.model as model

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    root = os.path.dirname(os.path.abspath(__file__))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='blobs', template_engine='mako', paths=paths)
    config['routes.map'] = make_map()
    config['pylons.g'] = Globals()
    config['pylons.h'] = blobs.helpers
    tmpl_options = config['buffet.template_options']
    config['pylons.g'].sa_engine = engine_from_config(config, 'sqlalchemy.')
    model.meta.bind = config['pylons.g'].sa_engine


def make_app(global_conf, full_stack=True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether or not this application provides a full WSGI stack (by
        default, meaning it handles its own exceptions and errors).
        Disable full_stack when this application is "managed" by another
        WSGI middleware.

    ``app_conf``
        The application's local configuration. Normally specified in the
        [app:<name>] section of the Paste ini file (where <name>
        defaults to main).
    """
    load_environment(global_conf, app_conf)
    app = PylonsApp()
    if asbool(full_stack):
        app = ErrorHandler(app, global_conf, error_template=error_template, **config['pylons.errorware'])
        app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)
    app = RegistryManager(app)
    javascripts_app = StaticJavascripts()
    static_app = StaticURLParser(config['pylons.paths']['static_files'])
    app = Cascade([static_app, javascripts_app, app])
    return app


class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable.
        """
        pass