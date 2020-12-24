# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/deletedteam.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.db import models
from sentry.db.models import sane_repr, BoundedBigIntegerField
from sentry.models.deletedentry import DeletedEntry

class DeletedTeam(DeletedEntry):
    """
    This model tracks an intent to delete. If an org is marked pending_delete
    through the UI, a deletedteam is created to log this deletion.

    This model does not account for aborted or failed deletions and is currently
    unable to log deletions that occur implicity (i.e. when the sole parent object
    is deleted, the child is also marked for deletion as well).
    """
    name = models.CharField(max_length=64, null=True)
    slug = models.CharField(max_length=50, null=True)
    organization_id = BoundedBigIntegerField(null=True)
    organization_name = models.CharField(max_length=64, null=True)
    organization_slug = models.CharField(max_length=50, null=True)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_deletedteam'

    __repr__ = sane_repr('date_deleted', 'slug', 'reason')