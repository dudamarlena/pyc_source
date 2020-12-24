# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/mrlpy/meventdispatch.py
# Compiled at: 2017-08-11 20:26:07


class MEventDispatch(object):
    """
    Generic event dispatcher which listen and dispatch events
    """

    def __init__(self):
        self._events = dict()

    def has_listener(self, event_type, listener):
        """
        Return true if listener is register to event_type
        """
        if event_type in self._events.keys():
            return listener in self._events[event_type]
        else:
            return False

    def dispatch_event(self, event):
        """
        Dispatch an instance of MEvent class
        """
        if event.type in self._events.keys():
            listeners = self._events[event.type]
            for listener in listeners:
                listener(event)

    def add_event_listener(self, event_type, listener):
        """
        Add an event listener for an event type
        """
        if not self.has_listener(event_type, listener):
            listeners = self._events.get(event_type, [])
            listeners.append(listener)
            self._events[event_type] = listeners

    def remove_event_listener(self, event_type, listener):
        """
        Remove event listener.
        """
        if self.has_listener(event_type, listener):
            listeners = self._events[event_type]
            if len(listeners) == 1:
                del self._events[event_type]
            else:
                listeners.remove(listener)
                self._events[event_type] = listeners