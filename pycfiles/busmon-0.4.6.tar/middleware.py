# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/threebean/devel/busmon/busmon/config/middleware.py
# Compiled at: 2012-10-04 13:49:55
"""WSGI middleware initialization for the busmon application."""
import tg
from busmon.config.app_cfg import base_config
from busmon.config.environment import load_environment
from moksha.wsgi.middleware import make_moksha_middleware
from tw2.core import make_middleware as make_tw2_middleware
__all__ = [
 'make_app']
make_base_app = base_config.setup_tg_wsgi_app(load_environment)

def make_app(global_conf, full_stack=True, **app_conf):
    """
    Set busmon up with the settings found in the PasteDeploy configuration
    file used.

    :param global_conf: The global settings for busmon (those
        defined under the ``[DEFAULT]`` section).
    :type global_conf: dict
    :param full_stack: Should the whole TG2 stack be set up?
    :type full_stack: str or bool
    :return: The busmon application with all the relevant middleware
        loaded.

    This is the PasteDeploy factory for the busmon application.

    ``app_conf`` contains all the application-specific settings (those defined
    under ``[app:main]``.

    """
    if tg.__version__ < '2.1.0':
        wrap_app = lambda app: make_tw2_middleware(make_moksha_middleware(app, app_conf), default_engine='mako', res_prefix=tg.config.get('busmon.resource_path_prefix', '/busmon/resources/'))
    else:
        wrap_app = lambda app: make_moksha_middleware(app, app_conf)
    app = make_base_app(global_conf, full_stack=True, wrap_app=wrap_app, **app_conf)
    return app