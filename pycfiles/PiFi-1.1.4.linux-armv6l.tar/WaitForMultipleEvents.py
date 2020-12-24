# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pifi/WaitForMultipleEvents.py
# Compiled at: 2014-10-22 23:54:57
import threading

class WaitForMultipleEvents(object):

    def __init__(self, eventsToWatch):
        self.mEvtController = threading.Event()
        self.mEventsToWatch = eventsToWatch
        self.mLock = threading.Lock()

    def set(self, event):
        if event in self.mEventsToWatch:
            with self.mLock:
                event.set()
                self.mEvtController.set()

    def clear(self, event):
        if event in self.mEventsToWatch:
            with self.mLock:
                event.clear()
                self.mEvtController.clear()

    def clearAll(self):
        with self.mLock:
            for event in self.mEventsToWatch:
                event.clear()

            self.mEvtController.clear()

    def waitAny(self):
        self.mEvtController.wait()
        with self.mLock:
            evtMatches = [ e for e in self.mEventsToWatch if e.is_set() ]
        return evtMatches