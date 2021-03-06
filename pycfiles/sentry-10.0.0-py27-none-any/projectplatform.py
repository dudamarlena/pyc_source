# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/projectplatform.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.db import models
from django.utils import timezone
from sentry.db.models import Model, BoundedBigIntegerField, sane_repr

class ProjectPlatform(Model):
    """
    Tracks usage of a platform for a given project.

    Note: This model is used solely for analytics.
    """
    __core__ = False
    project_id = BoundedBigIntegerField()
    platform = models.CharField(max_length=64)
    date_added = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_projectplatform'
        unique_together = (('project_id', 'platform'), )

    __repr__ = sane_repr('project_id', 'platform')