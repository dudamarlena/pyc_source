# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/tests/models.py
# Compiled at: 2017-09-07 07:30:48
from django.db import models

class Enum(models.Model):
    title = models.CharField(max_length=64)


class EnumItem(models.Model):
    enum = models.ForeignKey(Enum, related_name='items')
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=128)