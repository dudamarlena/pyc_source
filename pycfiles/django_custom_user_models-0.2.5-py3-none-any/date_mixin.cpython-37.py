# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\models\date_mixin.py
# Compiled at: 2020-01-09 10:05:00
# Size of source mod 2**32: 737 bytes
from django.db import models
import django.utils.translation as _
from jdatetime import datetime as jalali

class DateMixin(models.Model):
    date_verify = models.DateTimeField((_('verify date')),
      blank=True,
      null=True)
    date_joined = models.DateTimeField((_('join date')),
      blank=True,
      null=True,
      auto_now_add=True)

    @property
    def jalali_date_verify(self):
        return jalali.fromgregorian(datetime=(self.date_verify)).strftime('%d %b %Y')

    def jalali_date_joined(self):
        return jalali.fromgregorian(datetime=(self.date_joined)).strftime('%d %b %Y')

    class Meta:
        abstract = True