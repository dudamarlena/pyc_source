# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/dashboard.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db import models
from django.utils import timezone
from sentry.constants import ObjectStatus
from sentry.db.models import BoundedPositiveIntegerField, FlexibleForeignKey, Model, sane_repr

class Dashboard(Model):
    """
    A dashboard.
    """
    __core__ = True
    title = models.CharField(max_length=255)
    created_by = FlexibleForeignKey('sentry.User')
    organization = FlexibleForeignKey('sentry.Organization')
    date_added = models.DateTimeField(default=timezone.now)
    status = BoundedPositiveIntegerField(default=ObjectStatus.VISIBLE, choices=ObjectStatus.as_choices())

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_dashboard'
        unique_together = (('organization', 'title'), )

    __repr__ = sane_repr('organization', 'title')