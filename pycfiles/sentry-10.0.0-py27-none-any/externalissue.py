# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/externalissue.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db import models
from django.utils import timezone
from sentry.db.models import BoundedPositiveIntegerField, JSONField, Model, sane_repr

class ExternalIssue(Model):
    __core__ = False
    organization_id = BoundedPositiveIntegerField()
    integration_id = BoundedPositiveIntegerField()
    key = models.CharField(max_length=128)
    date_added = models.DateTimeField(default=timezone.now)
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    metadata = JSONField(null=True)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_externalissue'
        unique_together = (('organization_id', 'integration_id', 'key'), )

    __repr__ = sane_repr('organization_id', 'integration_id', 'key')