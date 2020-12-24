# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/platformexternalissue.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db import models
from django.utils import timezone
from sentry.db.models import BoundedBigIntegerField, Model, sane_repr

class PlatformExternalIssue(Model):
    __core__ = False
    group_id = BoundedBigIntegerField()
    service_type = models.CharField(max_length=64)
    display_name = models.TextField()
    web_url = models.URLField()
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_platformexternalissue'
        unique_together = (('group_id', 'service_type'), )

    __repr__ = sane_repr('group_id', 'service_type', 'display_name', 'web_url')

    @classmethod
    def get_annotations(cls, group):
        external_issues = cls.objects.filter(group_id=group.id)
        annotations = []
        for ei in external_issues:
            annotations.append('<a href="%s">%s</a>' % (ei.web_url, ei.display_name))

        return annotations