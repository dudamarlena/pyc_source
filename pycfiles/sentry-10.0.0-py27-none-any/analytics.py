# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/receivers/analytics.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.db.models.signals import post_save
from sentry import analytics
from sentry.models import User

def capture_signal(type):

    def wrapped(instance, created, **kwargs):
        if created:
            analytics.record(type, instance)

    return wrapped


post_save.connect(capture_signal('user.created'), sender=User, dispatch_uid='analytics.user.created', weak=False)