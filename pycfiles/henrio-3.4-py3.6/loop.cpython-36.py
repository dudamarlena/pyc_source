# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\henrio\loop.py
# Compiled at: 2017-12-18 21:46:07
# Size of source mod 2**32: 7192 bytes
import time, typing
from collections import deque
from concurrent.futures import CancelledError
from heapq import heappop, heappush
from inspect import iscoroutine, isawaitable
from traceback import print_exc
from .bases import AbstractLoop
from .futures import Task, Future
from .yields import sleep
__all__ = [
 'BaseLoop']

class BaseLoop(AbstractLoop):

    def __init__(self):
        self._queue = deque()
        self._tasks = deque()
        self._futures = list()
        self._timers = list()
        self._readers = dict()
        self._writers = dict()
        self.running = 0
        self.threadpool = None
        self.processpool = None

    def time(self):
        """Get the current loop time, relative and monotonic. Speed up the loop by increasing increments"""
        return time.monotonic()

    def sleep(self, amount):
        """Sleep"""
        return time.sleep(amount)

    def run_until_complete(self, starting_task: typing.Union[(typing.Generator, typing.Awaitable)]):
        """Run an awaitable/generator until it is complete and return its value. Raise if the task raises"""
        try:
            self.running += 1
            if not isinstance(starting_task, Future):
                starting_task = Task(starting_task, None)
            if starting_task not in self._tasks:
                self._queue.appendleft(starting_task)
            while not starting_task.complete and not starting_task.cancelled:
                self._loop_once()

            return starting_task.result()
        finally:
            if self.running:
                self.running -= 1

    def run_forever(self):
        """Run the current tasks queue forever"""
        try:
            if self.running:
                raise RuntimeError('Loop is already running!')
            else:
                self.running += 1
            while (self._queue or self._tasks or self._timers or self._readers or self._writers) and self.running:
                self._loop_once()

        finally:
            if self.running:
                self.running -= 1

    def _loop_once(self):
        """Check timers, IO, and run the queue once"""
        self._queue.extend(self._tasks)
        self._tasks.clear()
        while self._timers:
            if self._timers[0][0].cancelled or self._timers[0][0].complete:
                task, _ = heappop(self._timers)
            else:
                if self._timers[0][1] < self.time():
                    task, _ = heappop(self._timers)
                    self._tasks.append(task)
                else:
                    break

        for future, task in self._futures.copy():
            if future.complete or future.cancelled:
                self._tasks.append(task)
                self._futures.remove((future, task))

        self._poll()
        while self._queue:
            task = self._queue.popleft()
            if not task.cancelled and not task.complete:
                try:
                    if task._throw_later:
                        task._data = task.throw(task._throw_later)
                    else:
                        task._data = task.send(task._data)
                except StopIteration as err:
                    task.set_result(err.value)
                except CancelledError as err:
                    task.cancelled = True
                    task.set_exception(err)
                except Exception as err:
                    task.set_exception(err)
                    print_exc()
                else:
                    if isinstance(task._data, tuple):
                        command, *args = task._data
                        if command == 'sleep':
                            heappush(self._timers, (
                             task, self.time() + task._data[1]))
                        else:
                            if command == 'loop':
                                task._data = self
                            else:
                                if command == 'current_task':
                                    task._data = task
                                else:
                                    try:
                                        task._data = (getattr(self, command))(*args)
                                    except Exception as e:
                                        task._throw_later = e

                            if iscoroutine(task._data):
                                if command != 'create_task':
                                    self._tasks.append(task._data)
                            self._tasks.append(task)
                    else:
                        if task._data is None:
                            self._tasks.append(task)
                        else:
                            if isinstance(task._data, Future):
                                self._futures.append((task._data, task))
                            else:
                                raise RuntimeError('Invalid yield!')
            elif task.cancelled:
                task.close()

    def _poll(self):
        """Poll IO once, base loop doesn't handle IO, thus nothing happens"""
        if not self._tasks:
            if self._timers:
                if not self._timers[0][0].cancelled:
                    if self._timers[0][0].complete:
                        self.sleep(max(0.0, self._timers[0][1] - self.time()))

    def create_task(self, task: typing.Union[(typing.Generator, typing.Awaitable)]) -> Task:
        """Add a task to the internal queue, will get called eventually. Returns the awaitable wrapped in a Task"""
        if not isawaitable(task):
            raise TypeError('Task must be awaitable!')
        else:
            if not isinstance(task, Future):
                task = Task(task, None)
            if task not in self._queue:
                self._queue.append(task)
        return task

    def close(self):
        """Close the running event loop"""
        self.running = 0