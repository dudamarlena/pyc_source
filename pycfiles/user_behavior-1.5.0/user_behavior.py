# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/6z/y737zg156f53v6d096dlmv500000gn/T/pip-build-YeCYrE/user-behavior/user_behavior/models/user_behavior.py
# Compiled at: 2016-11-17 22:38:22
from __future__ import absolute_import
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .api_info import ApiInfo

class UserBehavior(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    api_info = models.ForeignKey(ApiInfo, related_name='user_behaviors', db_constraint=False, null=True)

    class Meta:
        db_table = 'user_behavior'

    def __unicode__(self):
        return str(self.id)