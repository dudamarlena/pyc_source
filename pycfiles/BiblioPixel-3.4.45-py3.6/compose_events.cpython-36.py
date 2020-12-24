# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/threads/compose_events.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 787 bytes
import functools, threading

def compose_events(events, condition=all):
    """
    Compose a sequence of events into one event.

    Arguments:
        events:    a sequence of objects looking like threading.Event
        condition: a function taking a sequence of bools and returning a bool.
    """
    events = list(events)
    master_event = threading.Event()

    def changed():
        if condition(e.is_set() for e in events):
            master_event.set()
        else:
            master_event.clear()

    def add_changed(f):

        @functools.wraps(f)
        def wrapped():
            f()
            changed()

        return wrapped

    for e in events:
        e.set = add_changed(e.set)
        e.clear = add_changed(e.clear)

    changed()
    return master_event