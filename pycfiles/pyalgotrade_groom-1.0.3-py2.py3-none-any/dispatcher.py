# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/dispatcher.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
from pyalgotrade import utils
from pyalgotrade import observer
from pyalgotrade import dispatchprio

class Dispatcher(object):

    def __init__(self):
        self.__subjects = []
        self.__stop = False
        self.__startEvent = observer.Event()
        self.__idleEvent = observer.Event()
        self.__currDateTime = None
        return

    def getCurrentDateTime(self):
        return self.__currDateTime

    def getStartEvent(self):
        return self.__startEvent

    def getIdleEvent(self):
        return self.__idleEvent

    def stop(self):
        self.__stop = True

    def getSubjects(self):
        return self.__subjects

    def addSubject(self, subject):
        if subject in self.__subjects:
            return
        if subject.getDispatchPriority() is dispatchprio.LAST:
            self.__subjects.append(subject)
        else:
            pos = 0
            for s in self.__subjects:
                if s.getDispatchPriority() is dispatchprio.LAST or subject.getDispatchPriority() < s.getDispatchPriority():
                    break
                pos += 1

            self.__subjects.insert(pos, subject)
        subject.onDispatcherRegistered(self)

    def __dispatchSubject(self, subject, currEventDateTime):
        ret = False
        if not subject.eof() and subject.peekDateTime() in (None, currEventDateTime):
            ret = subject.dispatch() is True
        return ret

    def __dispatch(self):
        smallestDateTime = None
        eof = True
        eventsDispatched = False
        for subject in self.__subjects:
            if not subject.eof():
                eof = False
                smallestDateTime = utils.safe_min(smallestDateTime, subject.peekDateTime())

        if not eof:
            self.__currDateTime = smallestDateTime
            for subject in self.__subjects:
                if self.__dispatchSubject(subject, smallestDateTime):
                    eventsDispatched = True

        return (
         eof, eventsDispatched)

    def run(self):
        try:
            for subject in self.__subjects:
                subject.start()

            self.__startEvent.emit()
            while not self.__stop:
                eof, eventsDispatched = self.__dispatch()
                if eof:
                    self.__stop = True
                elif not eventsDispatched:
                    self.__idleEvent.emit()

        finally:
            for subject in self.__subjects:
                subject.stop()

            for subject in self.__subjects:
                subject.join()