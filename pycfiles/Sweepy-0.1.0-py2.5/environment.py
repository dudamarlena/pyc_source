# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sweepy/config/environment.py
# Compiled at: 2009-10-21 07:41:19
"""Pylons environment configuration"""
import os
from mako.lookup import TemplateLookup
from pylons import config
from pylons.error import handle_mako_error
import sweepy.lib.app_globals as app_globals, sweepy.lib.helpers
from sweepy.config.routing import make_map

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='sweepy', paths=paths)
    config['routes.map'] = make_map()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.h'] = sweepy.lib.helpers
    config['pylons.app_globals'].mako_lookup = TemplateLookup(directories=paths['templates'], error_handler=handle_mako_error, module_directory=os.path.join(app_conf['cache_dir'], 'templates'), input_encoding='utf-8', default_filters=['escape'], imports=[
     'from webhelpers.html import escape'])