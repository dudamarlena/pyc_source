# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sentry_mailagain/models.py
# Compiled at: 2013-08-30 09:23:09
from django.db import models
from sentry.models import Group

class NotificationEvent(models.Model):
    group = models.ForeignKey(Group)
    notified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'notified_at'