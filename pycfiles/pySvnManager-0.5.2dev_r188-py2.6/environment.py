# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/config/environment.py
# Compiled at: 2010-08-08 03:18:43
"""Pylons environment configuration"""
import os
from mako.lookup import TemplateLookup
from pylons.configuration import PylonsConfig
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config
import pysvnmanager.lib.app_globals as app_globals, pysvnmanager.lib.helpers
from pysvnmanager.config.routing import make_map
from pysvnmanager.model import init_model

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    config = PylonsConfig()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    config.init_app(global_conf, app_conf, package='pysvnmanager', paths=paths)
    config['routes.map'] = make_map(config)
    config['pylons.app_globals'] = app_globals.Globals(config)
    config['pylons.h'] = pysvnmanager.lib.helpers
    import pylons
    pylons.cache._push_object(config['pylons.app_globals'].cache)
    config['pylons.app_globals'].mako_lookup = TemplateLookup(directories=paths['templates'], error_handler=handle_mako_error, module_directory=os.path.join(app_conf['cache_dir'], 'templates'), input_encoding='utf-8', default_filters=['escape'], imports=[
     'from webhelpers.html import escape'])
    if 'sqlalchemy.url' in config:
        engine = engine_from_config(config, 'sqlalchemy.')
    else:
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///%(here)s/db/fallback.db' % config)
    init_model(engine)
    if engine.url.drivername in ('sqlite', ) and not os.path.exists(engine.url.database):
        if not os.path.exists(os.path.dirname(engine.url.database)):
            os.makedirs(os.path.dirname(engine.url.database))
        from pysvnmanager.model.meta import Session, metadata, Base
        Base.metadata.create_all(bind=Session.bind)
    config['pylons.strict_tmpl_context'] = False
    return config