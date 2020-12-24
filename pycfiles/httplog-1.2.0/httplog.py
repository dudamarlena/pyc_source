# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\cd2\env\lib\site-packages\httplog\models\httplog.py
# Compiled at: 2016-11-28 22:21:48
from __future__ import absolute_import
from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField

class HttpLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    client = JSONField(default={}, null=True, blank=True)
    server = JSONField(default={}, null=True, blank=True)
    request = JSONField(default={}, null=True, blank=True)
    response = JSONField(default={}, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    user = models.ForeignKey(User, related_name='httplogs', db_constraint=False, null=True)

    class Meta:
        db_table = 'httplog'