# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/threads/task_thread.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 820 bytes
import collections, threading
from . import runnable

class Task(object):

    def __init__(self, task=None, event=None):
        self.task = task or (lambda : None)
        self.event = event or threading.Event()

    def run(self, next_task):
        """Wait for the event, run the task, trigger the next task."""
        self.event.wait()
        self.task()
        self.event.clear()
        next_task.event.set()


class TaskThread(runnable.LoopThread):

    def __init__(self, producer_task, consumer_task, daemon=True, **kwds):
        (super().__init__)(daemon=daemon, **kwds)
        self.producer_task = producer_task
        self.consumer_task = consumer_task

    def produce(self):
        self.producer_task.run(self.consumer_task)

    def run_once(self):
        self.consumer_task.run(self.producer_task)