# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/authprovider.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from bitfield import BitField
from django.db import models
from django.utils import timezone
from sentry.db.models import BoundedPositiveIntegerField, EncryptedJsonField, FlexibleForeignKey, Model, sane_repr

class AuthProvider(Model):
    __core__ = True
    organization = FlexibleForeignKey('sentry.Organization', unique=True)
    provider = models.CharField(max_length=128)
    config = EncryptedJsonField()
    date_added = models.DateTimeField(default=timezone.now)
    sync_time = BoundedPositiveIntegerField(null=True)
    last_sync = models.DateTimeField(null=True)
    default_role = BoundedPositiveIntegerField(default=50)
    default_global_access = models.BooleanField(default=True)
    default_teams = models.ManyToManyField('sentry.Team', blank=True)
    flags = BitField(flags=(('allow_unlinked', 'Grant access to members who have not linked SSO accounts.'), ), default=0)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_authprovider'

    __repr__ = sane_repr('organization_id', 'provider')

    def __unicode__(self):
        return self.provider

    def get_provider(self):
        from sentry.auth import manager
        return manager.get(self.provider, **self.config)

    def get_audit_log_data(self):
        return {'provider': self.provider, 'config': self.config}