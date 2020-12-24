# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/commitfilechange.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db import models
from sentry.db.models import BoundedPositiveIntegerField, FlexibleForeignKey, Model, sane_repr
COMMIT_FILE_CHANGE_TYPES = frozenset(('A', 'D', 'M'))

class CommitFileChange(Model):
    __core__ = False
    organization_id = BoundedPositiveIntegerField(db_index=True)
    commit = FlexibleForeignKey('sentry.Commit')
    filename = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=(('A', 'Added'), ('D', 'Deleted'), ('M', 'Modified')))

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_commitfilechange'
        unique_together = (('commit', 'filename'), )

    __repr__ = sane_repr('commit_id', 'filename')

    @staticmethod
    def is_valid_type(value):
        return value in COMMIT_FILE_CHANGE_TYPES