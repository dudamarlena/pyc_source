# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/special_coverage/managers.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 760 bytes
from django.db import models
from django.utils import timezone

class SpecialCoverageManager(models.Manager):

    def get_by_identifier(self, identifier):
        identifier_id = identifier.split('.')[(-1)]
        return super(SpecialCoverageManager, self).get_queryset().get(id=identifier_id)

    def active(self):
        qs = super(SpecialCoverageManager, self).get_queryset()
        now = timezone.now()
        return qs.filter(start_date__lte=now, end_date__gte=now) | qs.filter(start_date__lte=now, end_date__isnull=True)

    def inactive(self):
        qs = super(SpecialCoverageManager, self).get_queryset()
        now = timezone.now()
        return qs.filter(start_date__lte=now, end_date__lte=now)