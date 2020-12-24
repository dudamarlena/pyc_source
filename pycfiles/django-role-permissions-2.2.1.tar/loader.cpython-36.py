# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filipeximenes/Projects/django-role-permissions/rolepermissions/loader.py
# Compiled at: 2018-12-02 06:53:46
# Size of source mod 2**32: 812 bytes
from __future__ import unicode_literals
import inspect
from importlib import import_module
from pydoc import locate
from django.conf import settings

def get_app_name(app_name):
    """
    Returns a app name from new app config if is
    a class or the same app name if is not a class.
    """
    type_ = locate(app_name)
    if inspect.isclass(type_):
        return type_.name
    else:
        return app_name


def load_roles_and_permissions():
    if hasattr(settings, 'ROLEPERMISSIONS_MODULE'):
        import_module(settings.ROLEPERMISSIONS_MODULE)
    for app_name in settings.INSTALLED_APPS:
        if app_name is not 'rolepermissions':
            app_name = get_app_name(app_name)
            try:
                import_module('.permissions', app_name)
            except ImportError:
                pass