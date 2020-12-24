# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/grouprulestatus.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.db import models
from django.utils import timezone
from sentry.db.models import FlexibleForeignKey, Model, sane_repr

class GroupRuleStatus(Model):
    __core__ = False
    ACTIVE = 0
    INACTIVE = 1
    project = FlexibleForeignKey('sentry.Project')
    rule = FlexibleForeignKey('sentry.Rule')
    group = FlexibleForeignKey('sentry.Group')
    status = models.PositiveSmallIntegerField(default=ACTIVE)
    date_added = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(null=True)

    class Meta:
        db_table = 'sentry_grouprulestatus'
        app_label = 'sentry'
        unique_together = (('rule', 'group'), )

    __repr__ = sane_repr('rule_id', 'group_id', 'status')