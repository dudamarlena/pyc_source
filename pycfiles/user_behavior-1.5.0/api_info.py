# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/6z/y737zg156f53v6d096dlmv500000gn/T/pip-build-YeCYrE/user-behavior/user_behavior/models/api_info.py
# Compiled at: 2016-11-17 22:38:22
from __future__ import absolute_import
from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField

class ApiInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    client = JSONField(default={}, null=True, blank=True)
    server = JSONField(default={}, null=True, blank=True)
    request = JSONField(default={}, null=True, blank=True)
    response = JSONField(default={}, null=True, blank=True)
    user = models.ForeignKey(User, related_name='user_behaviors', db_constraint=False, null=True)

    class Meta:
        db_table = 'api_info'