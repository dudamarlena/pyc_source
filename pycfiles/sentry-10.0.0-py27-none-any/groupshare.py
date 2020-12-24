# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/groupshare.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from uuid import uuid4
from django.conf import settings
from django.db import models
from django.utils import timezone
from sentry.db.models import FlexibleForeignKey, Model, BaseManager, sane_repr

def default_uuid():
    return uuid4().hex


class GroupShare(Model):
    """
    A Group that was shared publicly.
    """
    __core__ = False
    project = FlexibleForeignKey('sentry.Project')
    group = FlexibleForeignKey('sentry.Group', unique=True)
    uuid = models.CharField(max_length=32, unique=True, default=default_uuid)
    user = FlexibleForeignKey(settings.AUTH_USER_MODEL, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    objects = BaseManager()

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_groupshare'

    __repr__ = sane_repr('project_id', 'group_id', 'uuid')