# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foundry/mixins.py
# Compiled at: 2015-01-27 08:59:34
from django.db import models
from django.contrib.sites.models import get_current_site

class CachingMixin(models.Model):
    enable_caching = models.BooleanField(default=False, null=False)
    cache_type = models.CharField(max_length=32, default='all_users', choices=(
     ('all_users', 'All users'),
     ('anonymous_only', 'Anonymous only'),
     ('anonymous_and_authenticated', 'Anonymous and authenticated'),
     ('per_user', 'Per user')), help_text='All users - content is cached once for all users\n<br />\nAnonymous only - content is cached once only for anonymous users\n<br />\nAnonymous and authenticated - content is cached once for anonymous users and once for authenticated users\n<br />\nPer user - content is cached once for anonymous users and for each authenticated user individually')
    cache_timeout = models.PositiveIntegerField(default=60, help_text='Timeout in seconds')

    class Meta:
        abstract = True