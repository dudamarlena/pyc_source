# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/tests/models.py
# Compiled at: 2018-09-10 07:18:29
from django.db import models

class DummyModel(models.Model):
    title = models.CharField(max_length=32)
    code = models.CharField(max_length=32)


class DummyForeignModel(models.Model):
    title = models.CharField(max_length=32)
    points_to = models.ForeignKey(DummyModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=32)


class DummyOtherModel(models.Model):
    title = models.CharField(max_length=32)
    code = models.CharField(max_length=32)