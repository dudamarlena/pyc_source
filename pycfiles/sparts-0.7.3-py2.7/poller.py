# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/tasks/poller.py
# Compiled at: 2014-08-03 23:01:54
from .periodic import PeriodicTask
from threading import Event

class PollerTask(PeriodicTask):
    """A PeriodicTask oriented around monitoring a single value.
    
    Simply override `fetch`, and the `onValueChanged()` method will be called
    with the old and new values.  Additionally, the `getValue()` method can
    be called by other tasks to block until the values are ready.
    """

    def initTask(self):
        self.current_value = None
        self.fetched = Event()
        super(PollerTask, self).initTask()
        return

    def execute(self, context=None):
        new_value = self.fetch()
        if self.current_value != new_value:
            self.onValueChanged(self.current_value, new_value)
        self.current_value = new_value
        self.fetched.set()

    def onValueChanged(self, old_value, new_value):
        self.logger.debug('onValueChanged(%s, %s)', old_value, new_value)

    def fetch(self):
        self.logger.debug('fetch')
        return

    def getValue(self, timeout=None):
        self.fetched.wait(timeout)
        return self.current_value