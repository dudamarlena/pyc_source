# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/projectbookmark.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.conf import settings
from django.db import models
from django.utils import timezone
from sentry.db.models import FlexibleForeignKey, Model, BaseManager, sane_repr
from sentry.models import Project

class ProjectBookmark(Model):
    """
    Identifies a bookmark relationship between a user and an
    aggregated event (Group).
    """
    __core__ = True
    project = FlexibleForeignKey(Project, blank=True, null=True, db_constraint=False)
    user = FlexibleForeignKey(settings.AUTH_USER_MODEL)
    date_added = models.DateTimeField(default=timezone.now, null=True)
    objects = BaseManager()

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_projectbookmark'
        unique_together = ('project', 'user')

    __repr__ = sane_repr('project_id', 'user_id')