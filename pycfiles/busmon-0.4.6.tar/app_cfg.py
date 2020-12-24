# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/threebean/devel/busmon/busmon/config/app_cfg.py
# Compiled at: 2012-10-04 13:49:55
"""
Global configuration file for TG2-specific settings in busmon.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::

    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))

"""
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