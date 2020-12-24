# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-sparkle-external/django-sparkle-external/sparkle/models/managers.py
# Compiled at: 2014-07-01 07:17:15
# Size of source mod 2**32: 323 bytes
from django.db import models
from .query import VersionQuerySet

class VersionManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return VersionQuerySet(self.model, using=self._db)

    def active(self, channel=None):
        return self.get_queryset().active(channel=channel)