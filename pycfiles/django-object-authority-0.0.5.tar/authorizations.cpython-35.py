# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomeu/workspace/wdna/django-object-authority/django_object_authority/authorizations.py
# Compiled at: 2017-05-31 09:11:55
# Size of source mod 2**32: 2017 bytes
from django.db.models.base import ModelBase

class AlreadyAuthorizationRegistered(Exception):
    pass


class NoAuthorizationRegistered(Exception):
    pass


class Authorization(object):
    __doc__ = '\n    A Authorization object encapsulates an instance of a object permission.\n    Models are registered with the Authorization using the register() method.\n    Use unregister() method to clean Authorization classes registered.\n    '

    def __init__(self):
        self._registry = {}

    def register(self, model_or_iterable, authorization_class=None, **options):
        """Register model authorization"""
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [
             model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry and self._registry[model].registered:
                raise AlreadyAuthorizationRegistered('Model "{}" is already registered for authorization'.format(model.__name__))
            try:
                self._register(model, authorization_class)
            except Exception:
                self._registry[model].registered = False
                raise

    def unregister(self, model_or_iterable):
        """Unregister model authorization"""
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [
             model_or_iterable]
        for model in model_or_iterable:
            self._registry.pop(model)

    def get(self, model):
        """Get registered model"""
        try:
            return self._registry[model]
        except KeyError:
            raise NoAuthorizationRegistered('Model "{}" is not registered for authorization'.format(model.__name__))

    def _register(self, model, authorization_class):
        setattr(authorization_class, 'registered', True)
        self._registry[model] = authorization_class


authorization = Authorization()