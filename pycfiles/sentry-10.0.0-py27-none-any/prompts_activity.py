# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/prompts_activity.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db import models
from django.conf import settings
from django.utils import timezone
from sentry.db.models import BoundedPositiveIntegerField, FlexibleForeignKey, JSONField, Model, sane_repr

class PromptsActivity(Model):
    """ Records user interaction with various feature prompts in product"""
    __core__ = False
    organization_id = BoundedPositiveIntegerField(db_index=True)
    project_id = BoundedPositiveIntegerField(db_index=True)
    user = FlexibleForeignKey(settings.AUTH_USER_MODEL, null=False)
    feature = models.CharField(max_length=64, null=False)
    data = JSONField(default={})
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_promptsactivity'
        unique_together = (('user', 'feature', 'organization_id', 'project_id'), )

    __repr__ = sane_repr('user_id', 'feature')