# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/tasks/periodic.py
# Compiled at: 2015-02-07 04:24:14
from __future__ import absolute_import
from concurrent.futures import Future
from six.moves import queue
from sparts.counters import counter, samples, SampleType
from sparts.sparts import option
from sparts.timer import Timer
from sparts.vtask import VTask, TryLater
from threading import Event

class PeriodicTask(VTask):
    """Task that executes `execute` at a specified interval

    You must either override the `INTERVAL` (seconds) class attribute, or
    pass a --{OPT_PREFIX}-interval in order for your task to run.
    """
    INTERVAL = None
    execute_duration_ms = samples(windows=[60, 240], types=[
     SampleType.AVG, SampleType.MAX, SampleType.MIN])
    n_iterations = counter()
    n_slow_iterations = counter()
    n_try_later = counter()
    interval = option(type=float, metavar='SECONDS', default=lambda cls: cls.INTERVAL, help='How often this task should run [%(default)s] (s)')

    def execute(self, context=None):
        """Override this to perform some custom action periodically."""
        self.logger.debug('execute')

    def execute_async(self):
        f = Future()
        if self.running:
            self.__futures.put(f)
        else:
            f.set_exception(RuntimeError('Worker not running'))
        return f

    def has_pending(self):
        return self.__futures.qsize() > 0

    def initTask(self):
        self.stop_event = Event()
        self.__futures = queue.Queue()
        super(PeriodicTask, self).initTask()
        assert self.interval is not None, 'INTERVAL must be defined on %s or --%s-interval passed' % (
         self.name, self.name)
        return

    def stop(self):
        self.stop_event.set()
        super(PeriodicTask, self).stop()

    def _runloop(self):
        timer = Timer()
        timer.start()
        while not self.service._stop:
            try:
                result = self.execute()
                while self.__futures.qsize():
                    f = self.__futures.get()
                    f.set_result(result)

            except TryLater as e:
                if self._handle_try_later(e):
                    return
                continue
            except Exception as e:
                while self.__futures.qsize():
                    f = self.__futures.get()
                    f.set_exception(e)

                raise

            self.n_iterations.increment()
            self.execute_duration_ms.add(timer.elapsed * 1000)
            to_sleep = self.interval - timer.elapsed
            if to_sleep > 0:
                if self.stop_event.wait(to_sleep):
                    return
            else:
                self.n_slow_iterations.increment()
            timer.start()

    def _handle_try_later(self, e):
        self.n_try_later.increment()
        if e.after is not None:
            self.logger.debug('TryLater (%s) thrown.  Retrying in %.2fs', e.message, e.after)
        else:
            self.logger.debug('TryLater (%s) thrown.  Retrying now', e.message)
        return self.stop_event.wait(e.after)