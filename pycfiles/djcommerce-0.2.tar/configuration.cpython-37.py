# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\jeff\Desktop\CodingDojoPractice\CodingDojoWork\python_stack\django\Django_Commerce\django_commerce\djcommerce\models\configuration.py
# Compiled at: 2019-06-27 16:26:41
# Size of source mod 2**32: 393 bytes
from django.db import models

class ConfigurationOption(models.Model):
    description = models.CharField(max_length=50)

    class Meta:
        abstract = True


class Configuration(models.Model):
    name = models.CharField(max_length=15)
    options = models.ManyToManyField(ConfigurationOption, related_name='configurations')

    class Meta:
        abstract = True