# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\jeff\Desktop\CodingDojoPractice\CodingDojoWork\python_stack\django\Django_Commerce\django_commerce\djcommerce\models\profile.py
# Compiled at: 2019-06-27 16:26:41
# Size of source mod 2**32: 394 bytes
from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from .address import Address

class Profile(TimeStampedModel):
    user = models.ForeignKey((settings.AUTH_USER_MODEL),
      on_delete=(models.CASCADE))
    addresses = models.ManyToManyField(Address)

    class Meta:
        abstract = True