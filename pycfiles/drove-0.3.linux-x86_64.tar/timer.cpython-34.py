# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/util/timer.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1587 bytes
"""This module provides classes and function to run timers. A timer
is a periodic exection of a function without any return.
"""
import time, threading
from time import sleep
from six.moves._thread import start_new_thread

class Timer(object):

    def __init__(self, interval, fun, *args, **kwargs):
        """The Time class provide a threading based timer
        which repeat an event each interval seconds.

        :type interval: int
        :param interval: the number of seconds between two consecutive
            executions of the function.
        :type fun: callable
        :param fun: a callable object (i.e. a function) to run
            in each interval. Aditional arguments can be pass
            to the function too.

        Example:
            >>> def example(name):
            ...     print(name)
            >>> x = Timer(interval=10, fun=example, name="myname")
            >>> x.run()
            >>> x.stop()
        """
        self.interval = interval
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.running = False

    def _run(self):
        while self.running:
            self.fun(*self.args, **self.kwargs)
            sleep(self.interval)

    def run(self):
        self.running = True
        start_new_thread(self._run, ())

    def stop(self):
        self.running = False

    @staticmethod
    def wait(number_of_threads, seconds=10):
        while threading.active_count() > number_of_threads:
            time.sleep(seconds)