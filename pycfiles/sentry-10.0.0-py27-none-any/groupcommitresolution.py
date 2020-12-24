# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/groupcommitresolution.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.db import models
from django.utils import timezone
from sentry.db.models import BoundedPositiveIntegerField, Model, sane_repr

class GroupCommitResolution(Model):
    """
    When a Group is referenced via a commit, it's association is stored here.
    """
    __core__ = False
    group_id = BoundedPositiveIntegerField()
    commit_id = BoundedPositiveIntegerField(db_index=True)
    datetime = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'sentry_groupcommitresolution'
        app_label = 'sentry'
        unique_together = (('group_id', 'commit_id'), )

    __repr__ = sane_repr('group_id', 'commit_id')