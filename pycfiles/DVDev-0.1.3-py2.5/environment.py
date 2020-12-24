# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/config/environment.py
# Compiled at: 2009-04-17 21:14:22
"""Pylons environment configuration"""
import os
from genshi.template import TemplateLoader
from pylons import config
import dvdev.lib.app_globals as app_globals, dvdev.lib.helpers
from dvdev.config.routing import make_map

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='dvdev', paths=paths)
    config['routes.map'] = make_map()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.h'] = dvdev.lib.helpers
    config['pylons.app_globals'].genshi_loader = TemplateLoader(paths['templates'], auto_reload=True)