# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/models/async_process.py
# Compiled at: 2019-10-01 09:52:31
# Size of source mod 2**32: 1552 bytes
from datetime import datetime
from django.db import models
from tom_targets.models import Target
ASYNC_STATUS_PENDING = 'pending'
ASYNC_STATUS_CREATED = 'created'
ASYNC_STATUS_FAILED = 'failed'
ASYNC_TERMINAL_STATES = (ASYNC_STATUS_CREATED, ASYNC_STATUS_FAILED)

class AsyncError(Exception):
    __doc__ = '\n    An error occurred in an asynchronous process\n    '


class AsyncProcess(models.Model):
    process_type = models.CharField(null=True, blank=True, max_length=100)
    identifier = models.CharField(null=False, blank=False, max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default=ASYNC_STATUS_PENDING)
    terminal_timestamp = models.DateTimeField(null=True, blank=True)
    failure_message = models.CharField(max_length=255, blank=True)
    target = models.ForeignKey(Target, on_delete=(models.CASCADE), null=True, blank=True)

    def clean(self):
        self.process_type = self.__class__.__name__
        if self.status in ASYNC_TERMINAL_STATES:
            self.terminal_timestamp = datetime.now()

    def save(self, *args, **kwargs):
        self.full_clean()
        (super().save)(*args, **kwargs)

    def run(self):
        """
        Perform the potentially long-running task. Should raise AsyncError with
        an appropriate error message on failure.
        """
        raise NotImplementedError