# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/listenagain.py
# Compiled at: 2009-05-11 19:02:38
import sched, itertools

class ListenAgain(object):
    CONFIG_FILE_NAME = 'resonance_listenagain.cfg'
    EVENTS_TO_LOAD = 5
    REPEAT_STRING = '(repeat)'

    def __init__(self):
        """
        """
        self._scheduler = None
        return

    def __call__(self):
        """
        """
        self.reloadSchedule()
        self._scheduler.run()

    def reloadSchedule(self):
        for loadedeventinstance in self.filterEvents(loadedevents):
            archiver_instance = archiver(gcalevent, parking_folder, recording_stream)
            self._scheduler.addevent(archiver_instance, startTime=gcalevent.getStart())

        self._scheduler.addevent(self.getEndOfSequenceTime(loadedevents), self.reloadSchedule())

    def filterEvents(self, eventSequence):
        return itertools.ifilter(self.filterevent, eventSequence)

    def filterevent(self, theEventInstance):
        """
        Returns true if this is an event we are going to record.
        """
        if self.REPEAT_STRING in theEventInstance.getEvent().getTitle():
            return False
        return True