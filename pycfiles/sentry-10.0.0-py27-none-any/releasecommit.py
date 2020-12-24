# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/releasecommit.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from sentry.db.models import BoundedPositiveIntegerField, FlexibleForeignKey, Model, sane_repr

class ReleaseCommit(Model):
    __core__ = False
    organization_id = BoundedPositiveIntegerField(db_index=True)
    project_id = BoundedPositiveIntegerField(null=True)
    release = FlexibleForeignKey('sentry.Release')
    commit = FlexibleForeignKey('sentry.Commit')
    order = BoundedPositiveIntegerField()

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_releasecommit'
        unique_together = (('release', 'commit'), ('release', 'order'))

    __repr__ = sane_repr('release_id', 'commit_id', 'order')