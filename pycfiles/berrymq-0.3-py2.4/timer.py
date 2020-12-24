# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/berrymq/adapter/timer.py
# Compiled at: 2009-11-07 07:20:43
import berrymq, os, time, threading

class IntervalTimer(object):
    __module__ = __name__

    def __init__(self, id_name, interval):
        self.id_name = id_name
        self.interval = interval
        self.thread = threading.Thread(target=self._notify)
        self.thread.setDaemon(True)
        self.running = True
        self.thread.start()

    def _checkdir(self):
        while self.running:
            time.sleep(self.interval)
            berrymq.twitter('%s:tick' % self.id_name)

    def stop(self):
        self.running = False