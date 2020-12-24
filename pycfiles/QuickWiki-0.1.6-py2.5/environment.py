# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/quickwiki/config/environment.py
# Compiled at: 2009-02-23 12:50:50
"""Pylons environment configuration"""
import os
from mako.lookup import TemplateLookup
from pylons import config
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config
import quickwiki.lib.app_globals as app_globals, quickwiki.lib.helpers
from quickwiki.config.routing import make_map
from quickwiki.model import init_model

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='quickwiki', paths=paths)
    config['routes.map'] = make_map()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.h'] = quickwiki.lib.helpers
    config['pylons.app_globals'].mako_lookup = TemplateLookup(directories=paths['templates'], error_handler=handle_mako_error, module_directory=os.path.join(app_conf['cache_dir'], 'templates'), input_encoding='utf-8', default_filters=['escape'], imports=[
     'from webhelpers.html import escape'])
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)