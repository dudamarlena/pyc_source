# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ivan/projects/packages/django-async-tasks/async_tasks/management/commands/django_async_tasks.py
# Compiled at: 2016-06-25 09:56:50
from django.core.management.base import BaseCommand
from async_tasks.utils import consume_task_queue
import time

class Command(BaseCommand):

    def handle(self, *args, **options):
        timeout = 60
        end_time = time.time() + timeout
        while end_time > time.time():
            consume_task_queue()
            time.sleep(1)