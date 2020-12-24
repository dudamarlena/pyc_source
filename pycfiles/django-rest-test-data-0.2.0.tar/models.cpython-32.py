# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/danielwatkins/dev/django-rest-test-data/rest_test_data/models.py
# Compiled at: 2013-11-25 04:39:00
from django.db import models

class Simple(models.Model):
    str_attr = models.CharField(max_length=20)
    int_attr = models.IntegerField()
    date_attr = models.DateTimeField()


class Key(models.Model):
    f_key = models.ForeignKey('Simple', related_name='key')
    m2m = models.ManyToManyField('Simple', related_name='keys')