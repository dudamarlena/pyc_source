# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/models/event_context_manager.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1260 bytes
from contextlib import contextmanager, ExitStack

class EventContextManager(object):
    __doc__ = '\n        Event context manager class, to be used as follows:\n        \n         ecm = EventContextManager(model.event1, model.event2, ...)\n        \n         with ecm.ignore():\n             pass #do something here that will cause events to be ignored\n        \n         with ecm.hold():\n             pass #do something here that will cause events to be held back\n        \n    '
    events = []

    def __init__(self, *events):
        self.events = events

    @contextmanager
    def ignore(self):
        if len(self.events):
            with ExitStack() as (stack):
                for event in self.events:
                    stack.enter_context(event.ignore())

                yield
        else:
            yield

    @contextmanager
    def hold(self):
        if len(self.events):
            with ExitStack() as (stack):
                for event in self.events:
                    stack.enter_context(event.hold())

                yield
        else:
            yield