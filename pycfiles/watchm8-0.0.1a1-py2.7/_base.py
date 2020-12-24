# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/watchers/_base.py
# Compiled at: 2017-09-11 04:31:22
from logging import getLogger
from threading import Thread

class _BaseWatcher(object):

    def __init__(self):
        self._log = getLogger('%s.%s' % (self.__class__.__module__, self.__class__.__name__))

    def set_fan(self, event_fan):
        self._fan = event_fan

    def _emit(self, event):
        self._fan.emit(event, self)


class BaseWatcher(_BaseWatcher, Thread):

    def __init__(self):
        _BaseWatcher.__init__(self)
        Thread.__init__(self)
        self._stop_watcher = False

    def _run(self):
        raise NotImplementedError()

    def run(self):
        self._log.info('Starting watcher')
        self._run()
        self._log.info('Exiting watcher')

    def stop(self):
        self._log.info('Stopping watcher')
        self._stop_watcher = True