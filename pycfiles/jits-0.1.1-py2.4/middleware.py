# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jits/middleware.py
# Compiled at: 2008-03-14 17:21:35
import datetime, scheduler

class JitsMiddleware(object):
    __module__ = __name__

    def __init__(self):
        from django.conf import settings
        self.scheduler = scheduler.Scheduler(getattr(settings, 'JITS_THREADED', False), getattr(settings, 'JITS_NUM_THREADS', 10))
        self.delta = datetime.timedelta(seconds=getattr(settings, 'JITS_MIN_SECONDS', 5), minutes=getattr(settings, 'JITS_MIN_MINUTES', 0))
        self.last_check = datetime.datetime(2000, 1, 1, 1, 1, 1)

    def process_request(self, request):
        now = datetime.datetime.now()
        if now - self.last_check > self.delta:
            self.last_check = now
            self.scheduler.poll()
        return