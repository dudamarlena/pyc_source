# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/workspaces/workspace_django/django-celerybeat-status/celerybeat_status/helpers.py
# Compiled at: 2018-02-15 23:46:59
# Size of source mod 2**32: 951 bytes
from celery.beat import Service
from django.utils import timezone
import datetime, json

def get_periodic_tasks_info():
    from celery import current_app
    schedule = Service(current_app).get_scheduler().get_schedule()
    tasks = []
    for key, entry in schedule.items():
        is_due_tpl = entry.is_due()
        next_execution = timezone.now() + datetime.timedelta(seconds=is_due_tpl[1])
        next_execution = next_execution.replace(microsecond=0)
        tasks.append({'name': key, 
         'task': entry.task, 
         'args': '(' + ', '.join([json.dumps(arg) for arg in entry.args]) + ')', 
         'kwargs': json.dumps(entry.kwargs), 
         'is_due': is_due_tpl[0], 
         'next_execution': next_execution})

    return tasks