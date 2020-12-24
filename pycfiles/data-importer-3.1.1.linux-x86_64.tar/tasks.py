# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/tasks.py
# Compiled at: 2020-04-17 10:46:24
import os
try:
    from celery import Task
except ImportError:
    Task = object

from django.core.cache import cache
from data_importer.core import default_settings
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
try:
    from django.conf import settings
except ImportError as e:
    settings = None

try:
    LOCK_EXPIRE = settings.DATA_IMPORTER_TASK_LOCK_EXPIRE
except AttributeError:
    LOCK_EXPIRE = default_settings.DATA_IMPORTER_TASK_LOCK_EXPIRE

try:
    DATA_IMPORTER_QUEUE = settings.DATA_IMPORTER_QUEUE
except AttributeError:
    DATA_IMPORTER_QUEUE = default_settings.DATA_IMPORTER_QUEUE

acquire_lock = lambda lock_id: cache.add(lock_id, 'true', LOCK_EXPIRE)
release_lock = lambda lock_id: cache.delete(lock_id)

class DataImpoterTask(Task):
    """
    This tasks is executed by Celery.
    """
    name = 'data_importer_task'
    queue = DATA_IMPORTER_QUEUE
    time_limit = 900

    @staticmethod
    def send_email(subject='[Data Importer] was processed', body='', owner=None):
        email = EmailMessage(subject=subject, body=body, to=[
         owner.email], headers={'Content-Type': 'text/plain'})
        email.send()

    def run(self, importer=None, source='', owner=None, message='', send_email=True, **kwargs):
        if not importer:
            return
        self.parser = importer(source=source)
        lock_id = ('{0!s}-lock').format(self.name)
        if acquire_lock(lock_id):
            self.parser.is_valid()
            self.parser.save()
            message += '\n'
            if owner and owner.email and self.parser.errors:
                message += mark_safe(self.parser.errors)
            elif owner and owner.email and not self.parser.errors:
                message = 'Your file was imported with sucess'
            if hasattr(owner, 'email') and send_email:
                self.send_email(body=message, owner=owner)
            release_lock(lock_id)
        else:
            return 0