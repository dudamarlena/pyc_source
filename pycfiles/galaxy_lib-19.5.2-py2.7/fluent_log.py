# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/logging/fluent_log.py
# Compiled at: 2018-04-20 03:19:42
"""
Provides a `TraceLogger` implementation that logs to a fluentd collector
"""
import json, threading, time
try:
    from fluent.sender import FluentSender
except ImportError:
    FluentSender = None

FLUENT_IMPORT_MESSAGE = 'The Python fluent package is required to use this feature, please install it'

class FluentTraceLogger(object):

    def __init__(self, name, host='localhost', port=24224):
        assert FluentSender is not None, FLUENT_IMPORT_MESSAGE
        self.lock = threading.Lock()
        self.thread_local = threading.local()
        self.name = name
        self.sender = FluentSender(self.name, host=host, port=port)
        return

    def context_set(self, key, value):
        self.lock.acquire()
        if not hasattr(self.thread_local, 'context'):
            self.thread_local.context = {}
        self.thread_local.context[key] = value
        self.lock.release()

    def context_remove(self, key):
        self.lock.acquire()
        del self.thread_local.context[key]
        self.lock.release()

    def log(self, label, event_time=None, **kwargs):
        self.lock.acquire()
        if hasattr(self.thread_local, 'context'):
            kwargs.update(self.thread_local.context)
        self.lock.release()
        event_time = event_time or time.time()
        self.sender.emit_with_time(label, int(event_time), json.dumps(kwargs, default=str))