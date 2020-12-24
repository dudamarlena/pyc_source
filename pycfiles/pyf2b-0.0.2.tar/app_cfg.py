# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/config/app_cfg.py
# Compiled at: 2010-12-14 11:19:38
__doc__ = "\nGlobal configuration file for TG2-specific settings in pyf.services.\n\nThis file complements development/deployment.ini.\n\nPlease note that **all the argument values are strings**. If you want to\nconvert them into boolean, for example, you should use the\n:func:`paste.deploy.converters.asbool` function, as in::\n    \n    from paste.deploy.converters import asbool\n    setting = asbool(global_conf.get('the_setting'))\n \n"
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