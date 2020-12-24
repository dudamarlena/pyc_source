# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/den/project/django-stored-queryset/test/stored/models.py
# Compiled at: 2012-05-02 09:34:07
from django.db import models

class Rel0(models.Model):
    pass


class TModel(models.Model):
    headline = models.CharField(max_length=64)
    related = models.ManyToManyField('stored.rel0')