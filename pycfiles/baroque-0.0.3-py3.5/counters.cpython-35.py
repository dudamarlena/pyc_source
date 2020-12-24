# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/datastructures/counters.py
# Compiled at: 2017-03-23 17:35:51
# Size of source mod 2**32: 1120 bytes
from baroque.entities.event import Event

class EventCounter:
    __doc__ = 'A counter of events.'

    def __init__(self):
        self.events_count = 0
        self.events_count_by_type = dict()

    def increment_counting(self, event):
        """Counts an event

        Args:
            event (:obj:`baroque.entities.event.Event`): the event to be counted

        """
        assert isinstance(event, Event)
        self.events_count += 1
        t = type(event.type)
        if t in self.events_count_by_type:
            self.events_count_by_type[t] += 1
        else:
            self.events_count_by_type[t] = 1

    def count_all(self):
        """Tells how many events have been counted globally

        Returns:
            int

        """
        return self.events_count

    def count(self, eventtype):
        """Tells how many events have been counted of the specified type

        Args:
            eventtype (:obj:`baroque.entities.eventtype.EventType`): the type of events to be counted

        Returns:
            int

        """
        return self.events_count_by_type.get(type(eventtype), 0)