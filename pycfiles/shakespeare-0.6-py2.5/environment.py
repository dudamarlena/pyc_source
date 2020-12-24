# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/config/environment.py
# Compiled at: 2008-10-29 17:02:16
"""Pylons environment configuration"""
import os
from sqlalchemy import engine_from_config
from pylons import config
import shakespeare.lib.app_globals as app_globals, shakespeare.lib.helpers
from shakespeare.config.routing import make_map

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='shakespeare', template_engine='genshi', paths=paths)
    config['routes.map'] = make_map()
    config['pylons.g'] = app_globals.Globals()
    config['pylons.h'] = shakespeare.lib.helpers
    tmpl_options = config['buffet.template_options']
    config['pylons.g'].sa_engine = engine_from_config(config, 'sqlalchemy.')