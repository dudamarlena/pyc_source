# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/event_handler.py
# Compiled at: 2009-09-07 17:44:28


class EventHandler(object):
    """
    Class to connect events to event handlers.
    """
    __module__ = __name__

    def __init__(self):
        self.handlers = {}

    def connect(self, event_name, handler):
        """
        Connect an event handler to an event. Append it to handlers list.
        """
        try:
            self.handlers[event_name].append(handler)
        except KeyError:
            self.handlers[event_name] = [
             handler]

    def raiseEvent(self, event_name, *args):
        """
        Raiser an event: call each handler for this event_name.
        """
        if event_name not in self.handlers:
            return
        for handler in self.handlers[event_name]:
            handler(*args)