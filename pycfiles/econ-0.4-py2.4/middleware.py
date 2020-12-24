# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/www/config/middleware.py
# Compiled at: 2007-04-18 06:57:54
from paste import httpexceptions
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser
from paste.registry import RegistryManager
from paste.deploy.config import ConfigMiddleware, CONFIG
from paste.deploy.converters import asbool
from pylons.error import error_template
from pylons.middleware import ErrorHandler, ErrorDocuments, StaticJavascripts, error_mapper
import pylons.wsgiapp
from econ.www.config.environment import load_environment
import econ.www.lib.helpers, econ.www.lib.app_globals as app_globals

def make_app(global_conf, full_stack=True, **app_conf):
    """Create a WSGI application and return it
    
    global_conf is a dict representing the Paste configuration options, the
    paste.deploy.converters should be used when parsing Paste config options
    to ensure they're treated properly.
    
    """
    CONFIG.push_process_config({'app_conf': app_conf, 'global_conf': global_conf})
    config = load_environment(global_conf, app_conf)
    config.init_app(global_conf, app_conf, package='econ.www')
    config.template_engines = []
    config.add_template_engine('genshi', 'econ.www.templates', {})
    app = pylons.wsgiapp.PylonsApp(config, helpers=econ.www.lib.helpers, g=app_globals.Globals)
    g = app.globals
    app = ConfigMiddleware(app, {'app_conf': app_conf, 'global_conf': global_conf})
    if asbool(full_stack):
        app = httpexceptions.make_middleware(app, global_conf)
        app = ErrorHandler(app, global_conf, error_template=error_template, **config.errorware)
        app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)
    app = RegistryManager(app)
    static_app = StaticURLParser(config.paths['static_files'])
    javascripts_app = StaticJavascripts()
    app = Cascade([static_app, javascripts_app, app])
    return app