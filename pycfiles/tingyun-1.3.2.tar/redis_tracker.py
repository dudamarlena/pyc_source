# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/ammunition/redis_tracker.py
# Compiled at: 2016-06-30 06:13:10
"""this module used to wrap the specify method to RedisTrace

"""
from tingyun.armoury.ammunition.timer import Timer
from tingyun.armoury.ammunition.tracker import current_tracker
from tingyun.logistics.warehouse.redis_node import RedisNode
from tingyun.logistics.basic_wrapper import wrap_object, FunctionWrapper

class RedisTrace(Timer):
    """
    """

    def __init__(self, tracker, command):
        """
        :return:
        """
        super(RedisTrace, self).__init__(tracker)
        self.command = command

    def create_node(self):
        """
        :return:
        """
        tracker = current_tracker()
        if tracker:
            tracker.redis_time = self.duration
        return RedisNode(command=self.command, children=self.children, start_time=self.start_time, end_time=self.end_time, duration=self.duration, exclusive=self.exclusive)

    def terminal_node(self):
        return True


def redis_trace_wrapper(wrapped, command):
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
            with RedisTrace(tracker, _command):
                return wrapped(*args, **kwargs)
            return

    def literal_wrapper(wrapped, instance, args, kwargs):
        tracker = current_tracker()
        if tracker is None:
            return wrapped(*args, **kwargs)
        else:
            with RedisTrace(tracker, command):
                return wrapped(*args, **kwargs)
            return

    if callable(command):
        return FunctionWrapper(wrapped, dynamic_wrapper)
    return FunctionWrapper(wrapped, literal_wrapper)


def wrap_redis_trace(module, object_path, command):
    wrap_object(module, object_path, redis_trace_wrapper, (command,))