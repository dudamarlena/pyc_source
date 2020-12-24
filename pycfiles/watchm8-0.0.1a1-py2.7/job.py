# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/job.py
# Compiled at: 2017-09-11 10:07:34
from logging import getLogger
from time import sleep
from threading import Thread
from watchm8.event import EventFan

class Job(Thread):

    def __init__(self, watchers, _filter, dispatcher):
        Thread.__init__(self)
        self._watchers = watchers
        self._filter = _filter
        self._dispatcher = dispatcher
        self._log = getLogger('Job')
        self._fan = EventFan(self._filter)
        self._stop_job = False

    @property
    def watchers(self):
        return self._watchers

    @property
    def dispatcher(self):
        return self._dispatcher

    def run(self):
        self._log.info('Starting job')
        self._fan.subscribe(self._dispatcher)
        for w in self.watchers:
            w.set_fan(self._fan)

        self._log.info('Starting watchers')
        for w in self.watchers:
            w.start()

        self._log.info('Job started')
        while not self._stop_job:
            sleep(3)

        self._log.info('Stopping watchers')
        for w in self.watchers:
            w.stop()

        for w in self.watchers:
            w.join()

        self._log.info('Job stopped')

    def stop(self):
        self._stop_job = True