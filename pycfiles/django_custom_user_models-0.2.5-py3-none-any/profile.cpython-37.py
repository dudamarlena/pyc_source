# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\models\profile.py
# Compiled at: 2019-12-11 09:39:05
# Size of source mod 2**32: 345 bytes
from django.db import models
from django.conf import settings
import django.utils.translation as _

class Profile(models.Model):
    user = models.OneToOneField((settings.AUTH_USER_MODEL),
      on_delete=(models.CASCADE),
      verbose_name=(_('profile')))

    class Meta:
        abstract = True