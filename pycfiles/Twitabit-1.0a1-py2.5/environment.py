# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twitabit/config/environment.py
# Compiled at: 2008-01-19 12:54:35
"""Pylons environment configuration"""
import os
from pylons import config
import twitabit.lib.app_globals as app_globals, twitabit.lib.helpers
from twitabit.config.routing import make_map

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config`` object"""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='twitabit', template_engine='mako', paths=paths)
    config['pylons.g'] = app_globals.Globals()
    config['pylons.h'] = twitabit.lib.helpers
    config['routes.map'] = make_map()
    tmpl_options = config['buffet.template_options']