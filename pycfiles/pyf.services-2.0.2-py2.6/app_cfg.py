# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/config/app_cfg.py
# Compiled at: 2010-12-14 11:19:38
"""
Global configuration file for TG2-specific settings in pyf.services.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::
    
    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
 
"""
from tg.configuration import AppConfig
from pylons.configuration import config as tg_config
tg_config['templating.genshi.method'] = 'html'
import pyf.services
from pyf.services import model
from pyf.services.lib import app_globals, helpers
base_config = AppConfig()
base_config.renderers = []
base_config.package = pyf.services
base_config.default_renderer = 'genshi'
base_config.renderers.append('genshi')
base_config.renderers.append('json')
base_config.use_sqlalchemy = True
base_config.model = model
base_config.DBSession = model.DBSession
base_config.auth_backend = 'sqlalchemy'
base_config.sa_auth.dbsession = model.DBSession
base_config.sa_auth.user_class = model.User
base_config.sa_auth.group_class = model.Group
base_config.sa_auth.permission_class = model.Permission
base_config.sa_auth.form_plugin = None
base_config.sa_auth.post_login_url = '/post_login'
base_config.sa_auth.post_logout_url = '/post_logout'
base_config.storage_dir = './storage'