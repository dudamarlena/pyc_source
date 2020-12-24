# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ikeda/.virtualenvs/rsyslog-monitor/django_spine/django-spine/examples/django_spine/spineapp/models.py
# Compiled at: 2012-07-17 10:44:29
from django.db import models
from django.utils.timezone import now
from bpmappers.djangomodel import ModelMapper

class Example(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, default=now(), editable=False)
    updated_at = models.DateTimeField(auto_now=True, default=now(), editable=False)


class ExampleMapper(ModelMapper):

    class Meta:
        model = Example