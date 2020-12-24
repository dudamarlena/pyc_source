# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/authidentity.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from sentry.db.models import EncryptedJsonField, FlexibleForeignKey, Model, sane_repr

class AuthIdentity(Model):
    __core__ = True
    user = FlexibleForeignKey(settings.AUTH_USER_MODEL)
    auth_provider = FlexibleForeignKey('sentry.AuthProvider')
    ident = models.CharField(max_length=128)
    data = EncryptedJsonField()
    last_verified = models.DateTimeField(default=timezone.now)
    last_synced = models.DateTimeField(default=timezone.now)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_authidentity'
        unique_together = (('auth_provider', 'ident'), ('auth_provider', 'user'))

    __repr__ = sane_repr('user_id', 'auth_provider_id')

    def __unicode__(self):
        return self.ident

    def get_audit_log_data(self):
        return {'user_id': self.user_id, 'data': self.data}

    def is_valid(self, member):
        if getattr(member.flags, 'sso:invalid'):
            return False
        if not getattr(member.flags, 'sso:linked'):
            return False
        if not self.last_verified:
            return False
        if self.last_verified < timezone.now() - timedelta(hours=24):
            return False
        return True

    def get_display_name(self):
        return self.user.get_display_name()

    def get_label(self):
        return self.user.get_label()