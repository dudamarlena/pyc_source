# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/threebean/devel/busmon/busmon/config/app_cfg.py
# Compiled at: 2012-10-04 13:49:55
__doc__ = "\nGlobal configuration file for TG2-specific settings in busmon.\n\nThis file complements development/deployment.ini.\n\nPlease note that **all the argument values are strings**. If you want to\nconvert them into boolean, for example, you should use the\n:func:`paste.deploy.converters.asbool` function, as in::\n\n    from paste.deploy.converters import asbool\n    setting = asbool(global_conf.get('the_setting'))\n\n"
from tg.configuration import AppConfig
import busmon
from busmon.lib import app_globals, helpers
base_config = AppConfig()
base_config.renderers = []
base_config.package = busmon
base_config.renderers.append('json')
base_config.default_renderer = 'mako'
base_config.renderers.append('mako')
base_config.use_sqlalchemy = False
base_config.use_toscawidgets = False
base_config.use_toscawidgets2 = True