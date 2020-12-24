# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/maharishi/config/middleware.py
# Compiled at: 2006-08-30 12:30:23
from paste import httpexceptions
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
from paste.registry import RegistryManager
from paste.deploy.config import ConfigMiddleware
from pylons.error import error_template
from pylons.middleware import ErrorHandler, ErrorDocuments, StaticJavascripts, error_mapper
import pylons.wsgiapp
from maharishi.config.environment import load_environment

def make_app(global_conf, **app_conf):
    """Create a WSGI application and return it
    
    global_conf is a dict representing the Paste configuration options, the
    paste.deploy.converters should be used when parsing Paste config options
    to ensure they're treated properly.
    
    """
    config = load_environment()
    config.init_app(global_conf, app_conf, package='maharishi')
    app = pylons.wsgiapp.PylonsApp(config)
    g = app.globals
    app = ConfigMiddleware(app, {'app_conf': app_conf, 'global_conf': global_conf})
    app = httpexceptions.make_middleware(app, global_conf)
    app = ErrorHandler(app, global_conf, error_template=error_template, **config.errorware)
    static_app = StaticURLParser(config.paths['static_files'])
    javascripts_app = StaticJavascripts()
    app = Cascade([static_app, javascripts_app, app])
    app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)
    app = RegistryManager(app)
    return app