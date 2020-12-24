# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idohyeon/Projects/motty/motty/app/models.py
# Compiled at: 2017-12-08 08:14:35
# Size of source mod 2**32: 1043 bytes
from datetime import datetime
from django.db import models

class Resource(models.Model):
    __doc__ = 'Resource manages actions.'
    name = models.CharField(unique=True, max_length=30)
    url = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return 'name: {0}, url: {1}'.format(self.name, self.url)


class Action(models.Model):
    __doc__ = 'Action produces responses to client, and all actions are managed by resource.'
    resource = models.ForeignKey(Resource, null=False, related_name='actions', on_delete=(models.CASCADE))
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=50)
    method = models.CharField(max_length=50)
    contentType = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(default=(datetime.now()))

    def __str__(self):
        return 'name: {0}, url: {1}, method: {2}, contentType: {3}, body: {4}, created_at: {5}'.format(self.name, self.url, self.method, self.contentType, self.body, self.created_at)