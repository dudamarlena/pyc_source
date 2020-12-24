# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/task.py
# Compiled at: 2018-06-20 21:27:44
"""
Task
"""
import sys
from time import time as _time
from heapq import heapify, heappush, heappop
import itertools
from .singleton import SingletonLogging
from .debugging import DebugContents, Logging, ModuleLogger, bacpypes_debugging
_debug = 0
_log = ModuleLogger(globals())
_task_manager = None
_unscheduled_tasks = []
if sys.platform in ('linux2', 'darwin'):
    from .event import WaitableEvent

    class _Trigger(WaitableEvent, Logging):

        def handle_read(self):
            if _debug:
                _Trigger._debug('handle_read')
            data = self.recv(1)
            if _debug:
                _Trigger._debug('    - data: %r', data)


else:
    _Trigger = None

class _Task(DebugContents, Logging):
    _debug_contents = ('taskTime', 'isScheduled')

    def __init__(self):
        self.taskTime = None
        self.isScheduled = False
        return

    def install_task(self, when=None, delta=None):
        global _task_manager
        global _unscheduled_tasks
        if when is None and delta is not None:
            if not _task_manager:
                raise RuntimeError('no task manager')
            when = _task_manager.get_time() + delta
        if when is None:
            when = self.taskTime
        if when is None:
            raise RuntimeError("schedule missing, use zero for 'now'")
        self.taskTime = when
        if not _task_manager:
            _unscheduled_tasks.append(self)
        else:
            _task_manager.install_task(self)
        return

    def process_task(self):
        raise RuntimeError('process_task must be overridden')

    def suspend_task(self):
        if not _task_manager:
            _unscheduled_tasks.remove(self)
        else:
            _task_manager.suspend_task(self)

    def resume_task(self):
        _task_manager.resume_task(self)

    def __lt__(self, other):
        return id(self) < id(other)


class OneShotTask(_Task):

    def __init__(self, when=None):
        _Task.__init__(self)
        self.taskTime = when


class OneShotDeleteTask(_Task):

    def __init__(self, when=None):
        _Task.__init__(self)
        self.taskTime = when


@bacpypes_debugging
def OneShotFunction(fn, *args, **kwargs):

    class OneShotFunctionTask(OneShotDeleteTask):

        def process_task(self):
            OneShotFunction._debug('process_task %r %s %s', fn, repr(args), repr(kwargs))
            fn(*args, **kwargs)

    task = OneShotFunctionTask()
    if not _task_manager:
        _unscheduled_tasks.append(task)
    else:
        task.install_task(delta=0)
    return task


def FunctionTask(fn, *args, **kwargs):
    _log.debug('FunctionTask %r %r %r', fn, args, kwargs)

    class _FunctionTask(OneShotDeleteTask):

        def process_task(self):
            _log.debug('process_task (%r %r %r)', fn, args, kwargs)
            fn(*args, **kwargs)

    task = _FunctionTask()
    _log.debug('    - task: %r', task)
    return task


@bacpypes_debugging
class RecurringTask(_Task):
    _debug_contents = ('taskInterval', 'taskIntervalOffset')

    def __init__(self, interval=None, offset=None):
        if _debug:
            RecurringTask._debug('__init__ interval=%r offset=%r', interval, offset)
        _Task.__init__(self)
        self.taskInterval = interval
        self.taskIntervalOffset = offset

    def install_task(self, interval=None, offset=None):
        if _debug:
            RecurringTask._debug('install_task interval=%r offset=%r', interval, offset)
        if interval is not None:
            self.taskInterval = interval
        if offset is not None:
            self.taskIntervalOffset = offset
        if self.taskInterval is None:
            raise RuntimeError('interval unset, use ctor or install_task parameter')
        if self.taskInterval <= 0.0:
            raise RuntimeError('interval must be greater than zero')
        if not _task_manager:
            if _debug:
                RecurringTask._debug('    - no task manager')
            _unscheduled_tasks.append(self)
        else:
            now = _task_manager.get_time() + 1e-06
            interval = self.taskInterval / 1000.0
            if self.taskIntervalOffset:
                offset = self.taskIntervalOffset / 1000.0
            else:
                offset = 0.0
            if _debug:
                RecurringTask._debug('    - now, interval, offset: %r, %r, %r', now, interval, offset)
            self.taskTime = now - offset + interval - (now - offset) % interval + offset
            if _debug:
                RecurringTask._debug('    - task time: %r', self.taskTime)
            _task_manager.install_task(self)
        return


@bacpypes_debugging
def RecurringFunctionTask(interval, fn, *args, **kwargs):
    if _debug:
        RecurringFunctionTask._debug('RecurringFunctionTask %r %r %r', fn, args, kwargs)

    class _RecurringFunctionTask(RecurringTask):

        def __init__(self, interval):
            RecurringTask.__init__(self, interval)

        def process_task(self):
            if _debug:
                RecurringFunctionTask._debug('process_task %r %r %r', fn, args, kwargs)
            fn(*args, **kwargs)

    task = _RecurringFunctionTask(interval)
    if _debug:
        RecurringFunctionTask._debug('    - task: %r', task)
    return task


@bacpypes_debugging
def recurring_function(interval, offset=None):

    def recurring_function_decorator(fn):

        class _RecurringFunctionTask(RecurringTask):

            def process_task(self):
                if _debug:
                    recurring_function._debug('process_task %r', fn)
                fn()

            def __call__(self, *args, **kwargs):
                fn(*args, **kwargs)

        task = _RecurringFunctionTask(interval, offset)
        task.install_task()
        return task

    return recurring_function_decorator


class TaskManager(SingletonLogging):

    def __init__(self):
        global _task_manager
        if _debug:
            TaskManager._debug('__init__')
        self.tasks = []
        if _Trigger:
            self.trigger = _Trigger()
        else:
            self.trigger = None
        _task_manager = self
        self.counter = itertools.count()
        if _unscheduled_tasks:
            for task in _unscheduled_tasks:
                task.install_task()

        return

    def get_time(self):
        if _debug:
            TaskManager._debug('get_time')
        return _time()

    def install_task(self, task):
        if _debug:
            TaskManager._debug('install_task %r @ %r', task, task.taskTime)
        if task.taskTime is None:
            raise RuntimeError('task time is None')
        if task.isScheduled:
            self.suspend_task(task)
        heappush(self.tasks, (task.taskTime, next(self.counter), task))
        if _debug:
            TaskManager._debug('    - tasks: %r', self.tasks)
        task.isScheduled = True
        if self.trigger:
            self.trigger.set()
        return

    def suspend_task(self, task):
        if _debug:
            TaskManager._debug('suspend_task %r', task)
        for i, (when, n, curtask) in enumerate(self.tasks):
            if task is curtask:
                if _debug:
                    TaskManager._debug('    - task found')
                del self.tasks[i]
                task.isScheduled = False
                heapify(self.tasks)
                break
        else:
            if _debug:
                TaskManager._debug('    - task not found')
            if self.trigger:
                self.trigger.set()

    def resume_task(self, task):
        if _debug:
            TaskManager._debug('resume_task %r', task)
        self.install_task(task)

    def get_next_task(self):
        """get the next task if there's one that should be processed,
        and return how long it will be until the next one should be
        processed."""
        if _debug:
            TaskManager._debug('get_next_task')
        now = _time()
        task = None
        delta = None
        if self.tasks:
            when, n, nxttask = self.tasks[0]
            if when <= now:
                heappop(self.tasks)
                task = nxttask
                task.isScheduled = False
                if self.tasks:
                    when, n, nxttask = self.tasks[0]
                    delta = max(when - now, 0.0)
            else:
                delta = when - now
        return (task, delta)

    def process_task(self, task):
        if _debug:
            TaskManager._debug('process_task %r', task)
        task.process_task()
        if isinstance(task, RecurringTask):
            task.install_task()
        elif isinstance(task, OneShotDeleteTask):
            del task