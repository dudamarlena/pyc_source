# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/config/environment.py
# Compiled at: 2007-10-25 16:53:48
"""Pylons environment configuration"""
import os
from pylons import config
import gazest.lib.app_globals as app_globals
from gazest.lib.wiki_util import extra_macros
from gazest.config.routing import make_map
from pprint import pprint
from pkg_resources import iter_entry_points
from gazest.lib.install_util import OPTIONS_COERCE
from paste.deploy.converters import asbool
from sqlalchemy import engine_from_config

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=[app_conf['extra_statics'], os.path.join(root, 'public')], templates=[app_conf['extra_templates'], os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='gazest', template_engine='mako', paths=paths)
    config['routes.map'] = make_map()
    config['pylons.g'] = app_globals.Globals()
    config['pylons.g'].sa_engine = engine_from_config(config, 'sqlalchemy.')
    import gazest.lib.helpers
    config['pylons.h'] = gazest.lib.helpers
    tmpl_options = config['buffet.template_options']
    for kind in OPTIONS_COERCE:
        coercer = kind[0]
        for opt in kind[1:]:
            config[opt] = coercer(config[opt])

    config['pylons.g'].config = config
    for ep in iter_entry_points('gazest.wiki_macros'):
        extra_macros[ep.name] = ep.load()