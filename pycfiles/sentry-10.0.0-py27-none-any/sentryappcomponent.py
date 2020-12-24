# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/sentryappcomponent.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.db import models
from sentry.db.models import EncryptedJsonField, FlexibleForeignKey, Model, UUIDField

class SentryAppComponent(Model):
    __core__ = True
    uuid = UUIDField(unique=True, auto_add=True)
    sentry_app = FlexibleForeignKey('sentry.SentryApp', related_name='components')
    type = models.CharField(max_length=64)
    schema = EncryptedJsonField()

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_sentryappcomponent'