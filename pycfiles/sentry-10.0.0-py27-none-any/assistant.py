# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/assistant.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.conf import settings
from django.db import models
from sentry.db.models import BoundedPositiveIntegerField, FlexibleForeignKey, Model, sane_repr

class AssistantActivity(Model):
    """Records user interactions with the assistant guides."""
    __core__ = False
    user = FlexibleForeignKey(settings.AUTH_USER_MODEL, null=False)
    guide_id = BoundedPositiveIntegerField()
    viewed_ts = models.DateTimeField(null=True)
    dismissed_ts = models.DateTimeField(null=True)
    useful = models.NullBooleanField(null=True)
    __repr__ = sane_repr('user', 'guide_id', 'viewed_ts', 'dismissed_ts', 'useful')

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_assistant_activity'
        unique_together = (('user', 'guide_id'), )