# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/apps.py
# Compiled at: 2019-07-02 16:47:10
from django.apps import AppConfig
from django.db import connections as djcs
from django.core.exceptions import ImproperlyConfigured

class ExplorerAppConfig(AppConfig):
    name = 'explorer'

    def ready(self):
        from explorer.schema import build_async_schemas
        _validate_connections()
        build_async_schemas()


def _get_default():
    from explorer.app_settings import EXPLORER_DEFAULT_CONNECTION
    return EXPLORER_DEFAULT_CONNECTION


def _get_explorer_connections():
    from explorer.app_settings import EXPLORER_CONNECTIONS
    return EXPLORER_CONNECTIONS


def _validate_connections():
    if _get_default() not in _get_explorer_connections().values():
        raise ImproperlyConfigured('EXPLORER_DEFAULT_CONNECTION is %s, but that alias is not present in the values of EXPLORER_CONNECTIONS' % _get_default())
    for name, conn_name in _get_explorer_connections().items():
        if conn_name not in djcs:
            raise ImproperlyConfigured('EXPLORER_CONNECTIONS contains (%s, %s), but %s is not a valid Django DB connection.' % (
             name, conn_name, conn_name))