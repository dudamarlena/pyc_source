# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/weborg/config/environment.py
# Compiled at: 2011-07-12 22:16:02
"""Pylons environment configuration"""
import os
from jinja2 import Environment, FileSystemLoader
from pylons.configuration import PylonsConfig
from sqlalchemy import engine_from_config
import weborg.lib.app_globals as app_globals, weborg.lib.helpers
from weborg.config.routing import make_map
from weborg.model import init_model

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='weborg', paths=paths)
    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    config['pylons.h'] = weborg.lib.helpers
    import pylons
    pylons.cache._push_object(config['pylons.app_globals'].cache)
    jinja2_env = Environment(loader=FileSystemLoader(paths['templates']))
    config['pylons.app_globals'].jinja2_env = jinja2_env
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)
    return config