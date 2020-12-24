# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/sentryappinstallation.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six, uuid
from django.db import models
from django.utils import timezone
from sentry.constants import SentryAppInstallationStatus
from sentry.db.models import BoundedPositiveIntegerField, FlexibleForeignKey, ParanoidModel, Model

def default_uuid():
    return six.binary_type(uuid.uuid4())


class SentryAppInstallationToken(Model):
    __core__ = False
    api_token = FlexibleForeignKey('sentry.ApiToken')
    sentry_app_installation = FlexibleForeignKey('sentry.SentryAppInstallation')

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_sentryappinstallationtoken'
        unique_together = (('sentry_app_installation', 'api_token'), )


class SentryAppInstallation(ParanoidModel):
    __core__ = True
    sentry_app = FlexibleForeignKey('sentry.SentryApp', related_name='installations')
    organization = FlexibleForeignKey('sentry.Organization', related_name='sentry_app_installations')
    api_grant = models.OneToOneField('sentry.ApiGrant', null=True, on_delete=models.SET_NULL, related_name='sentry_app_installation')
    api_token = models.OneToOneField('sentry.ApiToken', null=True, on_delete=models.SET_NULL, related_name='sentry_app_installation')
    uuid = models.CharField(max_length=64, default=default_uuid)
    status = BoundedPositiveIntegerField(default=SentryAppInstallationStatus.PENDING, choices=SentryAppInstallationStatus.as_choices(), db_index=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_sentryappinstallation'

    is_new = False

    def save(self, *args, **kwargs):
        self.date_updated = timezone.now()
        return super(SentryAppInstallation, self).save(*args, **kwargs)