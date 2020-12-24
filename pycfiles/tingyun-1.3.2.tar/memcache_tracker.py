# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/ammunition/memcache_tracker.py
# Compiled at: 2016-06-30 06:13:10
"""
"""
import logging
from tingyun.logistics.warehouse.memcache_node import MemcacheNode
from tingyun.logistics.basic_wrapper import wrap_object, FunctionWrapper
from tingyun.armoury.ammunition.timer import Timer
from tingyun.armoury.ammunition.tracker import current_tracker
console = logging.getLogger(__name__)

class MemcacheTrace(Timer):

    def __init__(self, tracker, command):
        super(MemcacheTrace, self).__init__(tracker)
        self.command = command

    def create_node(self):
        tracker = current_tracker()
        if tracker:
            tracker.memcache_time = self.duration
        return MemcacheNode(command=self.command, children=self.children, start_time=self.start_time, end_time=self.end_time, duration=self.duration, exclusive=self.exclusive)

    def terminal_node(self):
        return True


def memcached_trace_wrapper(wrapped, command):
    """
    :return:
    """

    def dynamic_wrapper(wrapped, instance, args, kwargs):
        tracker = current_tracker()
        if tracker is None:
            return wrapped(*args, **kwargs)
        else:
            if instance is not None:
                _command = command(instance, *args, **kwargs)
            else:
                _command = command(*args, **kwargs)
            with MemcacheTrace(tracker, _command):
                return wrapped(*args, **kwargs)
            return

    def literal_wrapper(wrapped, instance, args, kwargs):
        tracker = current_tracker()
        if tracker is None:
            return wrapped(*args, **kwargs)
        else:
            with MemcacheTrace(tracker, command):
                return wrapped(*args, **kwargs)
            return

    if callable(command):
        return FunctionWrapper(wrapped, dynamic_wrapper)
    return FunctionWrapper(wrapped, literal_wrapper)


def wrap_memcache_trace(module, object_path, command):
    wrap_object(module, object_path, memcached_trace_wrapper, (command,))