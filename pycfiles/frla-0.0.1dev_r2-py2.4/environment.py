# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/config/environment.py
# Compiled at: 2008-09-22 06:43:32
"""Pylons environment configuration"""
import os
from pylons import config
import frla.lib.app_globals as app_globals, frla.lib.helpers
from frla.config.routing import make_map

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='frla', template_engine='mako', paths=paths)
    config['routes.map'] = make_map()
    config['pylons.g'] = app_globals.Globals()
    config['pylons.h'] = frla.lib.helpers
    tmpl_options = config['buffet.template_options']