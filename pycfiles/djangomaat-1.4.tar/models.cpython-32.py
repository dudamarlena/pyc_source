# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/germanoguerrini/Developer/github/django-maat/djangomaat/models.py
# Compiled at: 2015-02-03 06:23:16
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class MaatRanking(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    typology = models.CharField(max_length=255, db_index=True)
    usable = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('content_type', 'typology', 'usable', 'position')

    def __str__(self):
        return 'Rank for {}'.format(self.content_object)