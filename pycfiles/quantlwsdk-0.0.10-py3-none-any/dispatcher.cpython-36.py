# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\dispatcher.py
# Compiled at: 2019-06-05 03:26:05
# Size of source mod 2**32: 4114 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import utils
from pyalgotrade import observer
from pyalgotrade import dispatchprio

class Dispatcher(object):

    def __init__(self):
        self._Dispatcher__subjects = []
        self._Dispatcher__stop = False
        self._Dispatcher__startEvent = observer.Event()
        self._Dispatcher__idleEvent = observer.Event()
        self._Dispatcher__currDateTime = None

    def getCurrentDateTime(self):
        return self._Dispatcher__currDateTime

    def getStartEvent(self):
        return self._Dispatcher__startEvent

    def getIdleEvent(self):
        return self._Dispatcher__idleEvent

    def stop(self):
        self._Dispatcher__stop = True

    def getSubjects(self):
        return self._Dispatcher__subjects

    def addSubject(self, subject):
        if subject in self._Dispatcher__subjects:
            return
        else:
            if subject.getDispatchPriority() is dispatchprio.LAST:
                self._Dispatcher__subjects.append(subject)
            else:
                pos = 0
                for s in self._Dispatcher__subjects:
                    if s.getDispatchPriority() is dispatchprio.LAST or subject.getDispatchPriority() < s.getDispatchPriority():
                        break
                    pos += 1

                self._Dispatcher__subjects.insert(pos, subject)
        subject.onDispatcherRegistered(self)

    def __dispatchSubject(self, subject, currEventDateTime):
        ret = False
        if not subject.eof():
            if subject.peekDateTime() in (None, currEventDateTime):
                ret = subject.dispatch() is True
        return ret

    def __dispatch(self):
        smallestDateTime = None
        eof = True
        eventsDispatched = False
        for subject in self._Dispatcher__subjects:
            if not subject.eof():
                eof = False
                smallestDateTime = utils.safe_min(smallestDateTime, subject.peekDateTime())

        if not eof:
            self._Dispatcher__currDateTime = smallestDateTime
            for subject in self._Dispatcher__subjects:
                if self._Dispatcher__dispatchSubject(subject, smallestDateTime):
                    eventsDispatched = True

        return (
         eof, eventsDispatched)

    def run(self):
        try:
            for subject in self._Dispatcher__subjects:
                subject.start()

            self._Dispatcher__startEvent.emit()
            while not self._Dispatcher__stop:
                eof, eventsDispatched = self._Dispatcher__dispatch()
                if eof:
                    self._Dispatcher__stop = True
                elif not eventsDispatched:
                    self._Dispatcher__idleEvent.emit()

        finally:
            self._Dispatcher__currDateTime = None
            for subject in self._Dispatcher__subjects:
                subject.stop()

            for subject in self._Dispatcher__subjects:
                subject.join()