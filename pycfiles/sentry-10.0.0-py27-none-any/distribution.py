# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/models/distribution.py
# Compiled at: 2019-09-04 11:05:35
from __future__ import absolute_import
from django.db import models
from django.utils import timezone
from sentry.db.models import Model, BoundedPositiveIntegerField, FlexibleForeignKey, sane_repr

class Distribution(Model):
    __core__ = False
    organization_id = BoundedPositiveIntegerField(db_index=True)
    release = FlexibleForeignKey('sentry.Release')
    name = models.CharField(max_length=64)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_distribution'
        unique_together = (('release', 'name'), )

    __repr__ = sane_repr('release', 'name')