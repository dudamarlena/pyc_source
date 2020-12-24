# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-sparkle-external/django-sparkle-external/sparkle/models/query.py
# Compiled at: 2014-07-01 07:17:15
# Size of source mod 2**32: 300 bytes
from django.utils.timezone import now
from django.db.models.query import QuerySet

class VersionQuerySet(QuerySet):

    def active(self, channel=None):
        qs = self.filter(publish_at__lte=now())
        if channel is None:
            return qs
        return qs.filter(channels__in=[channel])