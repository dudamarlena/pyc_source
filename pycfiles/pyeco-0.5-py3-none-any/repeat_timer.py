# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ecmc/repeat_timer.py
# Compiled at: 2016-04-06 13:02:53
import logging
from threading import Thread, Event
elasticache_logger = logging.getLogger('elasticache_logger')

class RepeatTimer(Thread):

    def __init__(self, name, interval, func, args=[], kwargs={}, daemonic=True, break_on_err=True):
        self.interval = interval
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.break_on_err = break_on_err
        self.stop_event = Event()
        super(RepeatTimer, self).__init__(name=name)
        self.setDaemon(daemonic)

    def run(self):
        while not self.stop_event.wait(self.interval):
            if self.stop_event.is_set():
                break
            try:
                self.func(*self.args, **self.kwargs)
            except Exception:
                if hasattr(self.func, '__name__'):
                    func_name = self.func.__name__
                else:
                    func_name = ''
                msg = '%s %s failed' % (str(self.func), func_name)
                elasticache_logger.exception(msg)
                if self.break_on_err:
                    break

    def stop_timer(self):
        self.stop_event.set()