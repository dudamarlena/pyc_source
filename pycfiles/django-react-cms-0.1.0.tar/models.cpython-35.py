# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-react-cms/react_cms/models.py
# Compiled at: 2017-01-09 12:56:08
# Size of source mod 2**32: 245 bytes
from django.db import models

class ContentResource(models.Model):
    name = models.CharField('Resource Name', max_length=100)
    path = models.CharField('Resource Path', max_length=1000)
    json = models.TextField('Label', blank=True, null=True)