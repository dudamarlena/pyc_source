# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andres/Dropbox/Development/Unholster/django-lookup/lookup/models.py
# Compiled at: 2013-12-09 15:32:54
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class Alias(models.Model):
    key = models.TextField(max_length=255)
    target_type = models.ForeignKey(ContentType)
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_type', 'target_id')

    class Meta:
        unique_together = ('key', 'target_type')


class Dummy(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name