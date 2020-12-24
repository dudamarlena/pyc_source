# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/dbmechanic/frameworks/tg2/test/TG2TestApp/tg2testapp/config/environment.py
# Compiled at: 2008-06-30 11:43:44
"""Pylons environment configuration"""
import os
from pylons import config
from pylons.i18n import ugettext
from genshi.filters import Translator
from tg import defaults
from sqlalchemy import engine_from_config
import tg2testapp.lib.app_globals as app_globals
from tg2testapp.model import init_model

def template_loaded(template):
    """Plug-in our i18n function to Genshi."""
    template.filters.insert(0, Translator(ugettext))


def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root, controllers=os.path.join(root, 'controllers'), static_files=os.path.join(root, 'public'), templates=[
     os.path.join(root, 'templates')])
    make_map = defaults.make_default_route_map
    config.init_app(global_conf, app_conf, package='tg2testapp', template_engine='genshi', paths=paths)
    config['routes.map'] = make_map()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.app_globals'].sa_engine = engine_from_config(config, 'sqlalchemy.')
    template_engine = 'genshi'
    template_engine_options = {}
    config['buffet.template_engines'].pop()
    config.add_template_engine(template_engine, 'tg2testapp.templates', template_engine_options)
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)
    from tg2testapp import model
    model.DBSession.configure(bind=config['pylons.app_globals'].sa_engine)
    model.metadata.bind = config['pylons.app_globals'].sa_engine