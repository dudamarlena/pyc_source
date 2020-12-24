# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/duashttp/router.py
# Compiled at: 2014-10-31 10:16:21
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
DUAS_ENABLE_DB_WRITE = getattr(settings, 'DUAS_ENABLE_DB_WRITE', False)
DUAS_DB_ROUTE_PREFIX = getattr(settings, 'DUAS_DB_ROUTE_PREFIX', 'unity_asset_server')

class UnityAssetServerRouter(object):
    """
    Router for unity asset server data base
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to duashttp.
        """
        if model._meta.app_label == 'duashttp':
            return DUAS_DB_ROUTE_PREFIX
        else:
            return

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to duashttp.
        """
        if model._meta.app_label == 'duashttp':
            if not DUAS_ENABLE_DB_WRITE:
                raise ImproperlyConfigured('Set `DUAS_ENABLE_DB_WRITE` to True in your settings to enable write operations on unity asset server database')
            return DUAS_DB_ROUTE_PREFIX
        return

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'duashttp' or obj2._meta.app_label == 'duashttp':
            return True
        return

    def allow_migrate(self, db, model):
        """
        Make sure the auth app only appears in the 'duashttp'
        database.
        """
        if db == DUAS_DB_ROUTE_PREFIX:
            return model._meta.app_label == 'duashttp'
        else:
            if model._meta.app_label == 'duashttp':
                return False
            return