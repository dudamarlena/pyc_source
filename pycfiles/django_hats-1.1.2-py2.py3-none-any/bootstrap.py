# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikehearing/GIT/django-hats/django_hats/bootstrap.py
# Compiled at: 2017-02-01 11:16:24
from importlib import import_module
import os, six
from django.conf import settings

class Bootstrapper(object):
    prefix = '_role_'
    _available_roles = {}

    @staticmethod
    def load():
        package_name = os.path.dirname(__file__)
        for app in settings.INSTALLED_APPS:
            if app is not package_name:
                try:
                    import_module('.roles', app)
                except ImportError:
                    pass

    @classmethod
    def register(cls, role_class):
        name = role_class.get_slug()
        if name not in cls._available_roles:
            cls._available_roles[name] = role_class
            return True
        raise ValueError('Role with name `%s` is already registered. Consider defining Meta.name to disambiguate.' % name)

    @classmethod
    def get_roles(cls):
        return [ klass for key, klass in six.iteritems(cls._available_roles) ]