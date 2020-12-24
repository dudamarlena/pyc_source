# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramzi/drf-social-auth/drf_social/models.py
# Compiled at: 2020-03-05 04:26:39
# Size of source mod 2**32: 877 bytes
import enum
from django.db import models

class Providers(str, enum.Enum):
    FACEBOOK = 'FACEBOOK'
    GOOGLE = 'GOOGLE'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class AuthProvider(models.Model):
    name = models.CharField(max_length=20)
    provider = models.CharField(choices=((p, p) for p in Providers), max_length=10, null=False, blank=False)
    client_id = models.CharField(max_length=100, null=False, blank=False)
    client_secret = models.CharField(max_length=100, null=False, blank=False)
    scopes = models.TextField(default='[]', null=False, blank=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        from drf_social.helpers import load_providers
        load_providers()