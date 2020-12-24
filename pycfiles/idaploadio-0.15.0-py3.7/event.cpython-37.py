# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/event.py
# Compiled at: 2020-04-15 05:32:36
# Size of source mod 2**32: 5375 bytes


class EventHook(object):
    __doc__ = '\n    Simple event class used to provide hooks for different types of events in Locust.\n\n    Here\'s how to use the EventHook class::\n\n        my_event = EventHook()\n        def on_my_event(a, b, **kw):\n            print("Event was fired with arguments: %s, %s" % (a, b))\n        my_event.add_listener(on_my_event)\n        my_event.fire(a="foo", b="bar")\n\n    If reverse is True, then the handlers will run in the reverse order\n    that they were inserted\n    '

    def __init__(self):
        self._handlers = []

    def add_listener(self, handler):
        self._handlers.append(handler)
        return handler

    def remove_listener(self, handler):
        self._handlers.remove(handler)

    def fire(self, reverse=False, **kwargs):
        if reverse:
            handlers = reversed(self._handlers)
        else:
            handlers = self._handlers
        for handler in handlers:
            handler(**kwargs)


class Events:
    request_success = EventHook
    request_failure = EventHook
    idapload_error = EventHook
    report_to_master = EventHook
    slave_report = EventHook
    hatch_complete = EventHook
    quitting = EventHook
    master_start_hatching = EventHook
    master_stop_hatching = EventHook
    idapload_start_hatching = EventHook
    idapload_stop_hatching = EventHook
    init = EventHook
    init_command_line_parser = EventHook

    def __init__(self):
        for name, value in vars(type(self)).items():
            if value == EventHook:
                setattr(self, name, value())