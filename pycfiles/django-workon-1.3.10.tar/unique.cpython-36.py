# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/models/unique.py
# Compiled at: 2019-01-30 08:47:42
# Size of source mod 2**32: 692 bytes
from django.db import models
__all__ = [
 'Unique', 'Singleton']

class Unique(models.Model):
    _cache = None

    class Meta:
        abstract = True

    @classmethod
    def get(cls):
        if cls._cache is None:
            instance = cls._meta.default_manager.first()
            if not instance:
                instance = cls()
            cls._cache = instance
        return cls._cache

    def save(self, *args, **kwargs):
        previous = self._meta.default_manager.first()
        if previous:
            self.pk = previous.pk
        (super().save)(*args, **kwargs)
        self._meta.model._cache = self


class Singleton(Unique):

    class Meta:
        abstract = True