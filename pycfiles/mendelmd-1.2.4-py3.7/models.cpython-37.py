# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/workers/models.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 788 bytes
from django.db import models
from datetime import datetime

class Worker(models.Model):
    name = models.CharField(max_length=30)
    provider = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    n_tasks = models.IntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=30)
    current_status = models.TextField(null=True, blank=True)
    worker_id = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    execution_time = models.TimeField(null=True)