# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-whatsnew/whatsnew/models.py
# Compiled at: 2014-04-03 15:26:47
from django.db import models
from .fields import VersionField
from django.utils.translation import gettext as _

class WhatsNew(models.Model):
    version = VersionField()
    content = models.TextField()
    expire = models.DateField(blank=True, null=True)
    enabled = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.version)

    class Meta:
        get_latest_by = 'id'
        verbose_name = _("What's New")
        verbose_name_plural = _("What's New")