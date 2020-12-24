# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/commit.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db import models
from django.utils import timezone
from sentry.db.models import BoundedPositiveIntegerField, FlexibleForeignKey, Model, sane_repr
from sentry.utils.cache import memoize
from sentry.utils.groupreference import find_referenced_groups

class Commit(Model):
    __core__ = False
    organization_id = BoundedPositiveIntegerField(db_index=True)
    repository_id = BoundedPositiveIntegerField()
    key = models.CharField(max_length=64)
    date_added = models.DateTimeField(default=timezone.now)
    author = FlexibleForeignKey('sentry.CommitAuthor', null=True)
    message = models.TextField(null=True)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_commit'
        index_together = (('repository_id', 'date_added'), )
        unique_together = (('repository_id', 'key'), )

    __repr__ = sane_repr('organization_id', 'repository_id', 'key')

    @memoize
    def title(self):
        if not self.message:
            return ''
        return self.message.splitlines()[0]

    @memoize
    def short_id(self):
        if len(self.key) == 40:
            return self.key[:7]
        return self.key

    def find_referenced_groups(self):
        return find_referenced_groups(self.message, self.organization_id)