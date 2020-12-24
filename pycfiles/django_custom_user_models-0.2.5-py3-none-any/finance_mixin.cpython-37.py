# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\models\finance_mixin.py
# Compiled at: 2019-12-11 09:45:43
# Size of source mod 2**32: 268 bytes
from django.db import models
import django.utils.translation as _

class FinanceMixin(models.Model):
    wallet = models.PositiveIntegerField((_('Credit of user')),
      default=0)

    class Meta:
        abstract = True