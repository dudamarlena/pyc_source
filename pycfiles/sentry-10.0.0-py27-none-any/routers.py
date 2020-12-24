# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/queue/routers.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import itertools, six
from celery import current_app
COUNTER_TASKS = set(['sentry.tasks.process_buffer.process_incr'])
TRIGGER_TASKS = set([
 'sentry.tasks.post_process.post_process_group',
 'sentry.tasks.post_process.plugin_post_process_group'])

class SplitQueueRouter(object):

    def __init__(self):
        queues = current_app.conf['CELERY_QUEUES']
        self.counter_queues = itertools.cycle([ q.name for q in queues if q.name.startswith('counters-') ])
        self.trigger_queues = itertools.cycle([ q.name for q in queues if q.name.startswith('triggers-') ])

    def route_for_task(self, task, *args, **kwargs):
        if task in COUNTER_TASKS:
            return {'queue': six.next(self.counter_queues)}
        else:
            if task in TRIGGER_TASKS:
                return {'queue': six.next(self.trigger_queues)}
            return