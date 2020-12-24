# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/config/environment.py
# Compiled at: 2011-03-30 09:31:00
"""Pylons environment configuration"""
import os
from mako.lookup import TemplateLookup
from pylons.configuration import PylonsConfig
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config
import argonaut.lib.app_globals as app_globals, argonaut.lib.helpers
from argonaut.config.routing import make_map
from argonaut.model import init_model
import argonaut.model.meta as meta
from paste.deploy.converters import asbool
from migrate.versioning.util import load_model
from migrate.versioning import exceptions, genmodel, schemadiff, schema

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='argonaut', paths=paths)
    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    config['pylons.h'] = argonaut.lib.helpers
    import pylons
    pylons.cache._push_object(config['pylons.app_globals'].cache)
    config['pylons.app_globals'].mako_lookup = TemplateLookup(directories=paths['templates'], error_handler=handle_mako_error, module_directory=os.path.join(app_conf['cache_dir'], 'templates'), input_encoding='utf-8', default_filters=['escape'], imports=[
     'from webhelpers.html import escape'])
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)
    return config