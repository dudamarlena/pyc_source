# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/pyenv/uvena_de/django_clear_memcache/models.py
# Compiled at: 2017-04-17 06:22:56
# Size of source mod 2**32: 498 bytes
from django.db import models
from django.utils.translation import ugettext_lazy as _

class ClearMemcache(models.Model):
    __doc__ = "This is a fake model, just to trick Django's admin to\n       have an easy changelist view"

    class Meta:
        managed = False
        app_label = 'django_clear_memcache'
        verbose_name = _('Clear Memcache')
        verbose_name_plural = _('Clear Memcache')