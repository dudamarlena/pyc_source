# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/umeboshi/tasks.py
# Compiled at: 2015-12-31 08:37:33
"""
django-umeboshi.tasks
~~~~~~~~~~~~~~~~~~~~~~~~~~

Tasks to run asynchronously via Celery
"""
from umeboshi.models import Event
from django.utils import timezone
from celery.task import task
from umeboshi.utils import lock

@task(ignore_result=True, soft_time_limit=300)
def process_event(event_id):
    with lock(event_id):
        event = Event.objects.get(pk=event_id)
        if event.status == Event.Status.CREATED:
            event.process()


@task(ignore_result=True)
def process_all_events():
    event_ids = Event.objects.filter(datetime_scheduled__lte=timezone.now(), status=Event.Status.CREATED).order_by('datetime_scheduled').values_list('pk', flat=True)
    for event_id in event_ids:
        process_event.delay(event_id)

    return len(event_ids)