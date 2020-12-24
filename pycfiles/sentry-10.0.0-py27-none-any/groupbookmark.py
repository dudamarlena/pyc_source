# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/groupbookmark.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.conf import settings
from django.db import models
from django.utils import timezone
from sentry.db.models import FlexibleForeignKey, Model, BaseManager, sane_repr

class GroupBookmark(Model):
    """
    Identifies a bookmark relationship between a user and an
    aggregated event (Group).
    """
    __core__ = False
    project = FlexibleForeignKey('sentry.Project', related_name='bookmark_set')
    group = FlexibleForeignKey('sentry.Group', related_name='bookmark_set')
    user = FlexibleForeignKey(settings.AUTH_USER_MODEL, related_name='sentry_bookmark_set')
    date_added = models.DateTimeField(default=timezone.now, null=True)
    objects = BaseManager()

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_groupbookmark'
        unique_together = (('project', 'user', 'group'), )

    __repr__ = sane_repr('project_id', 'group_id', 'user_id')