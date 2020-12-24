# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\django-microsip-base\django_microsip_base\django_microsip_base\libs\databases_routers_tests.py
# Compiled at: 2019-09-09 14:23:53
conexion_activa = '01-AD2007'

class MainRouter(object):
    """
    A router to control all database operations on models.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'config':
            return 'CONFIG'
        else:
            if model._meta.app_label == 'auth':
                return 'default'
            if model._meta.app_label == 'django':
                return 'default'
            if model._meta.app_label == 'models_base':
                if conexion_activa != None:
                    return '%s' % conexion_activa
            return

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'config':
            return 'CONFIG'
        else:
            if model._meta.app_label == 'auth':
                return 'default'
            if model._meta.app_label == 'django':
                return 'default'
            if model._meta.app_label == 'models_base':
                return '%s' % conexion_activa
            return

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        if obj1._meta.app_label == 'auth' and obj2._meta.app_label == 'django' or obj1._meta.app_label == 'django' and obj2._meta.app_label == 'auth':
            return True
        if obj1._meta.app_label == 'models_base' and obj2._meta.app_label == 'models_base':
            return True
        return False

    def allow_syncdb(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if model._meta.app_label == 'config' or 'CONFIG' in db:
            return False
        if model._meta.app_label == 'auth' and db != 'default':
            return False
        else:
            if model._meta.app_label == 'django' and db != 'default':
                return False
            else:
                if db == 'default' and model._meta.app_label == 'models_base':
                    return False
                return True

            return