# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/timer.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains a :class:`Timer` class"""
__all__ = [
 'Timer']
__docformat__ = 'restructuredtext'
import time, threading
from .log import Logger

class Timer(Logger):
    """
    Timer Object.

    Interval in seconds (The argument may be a floating point number for
    subsecond precision).
    If strict_timing is True, the timer will try to compensate for drifting
    due to the time it takes to execute function in each loop.
    """

    def __init__(self, interval, function, parent, strict_timing=True, *args, **kwargs):
        Logger.__init__(self, 'Timer on ' + function.__name__, parent)
        self.__lock = threading.Lock()
        self.__interval = interval
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs
        self.__loop = False
        self.__alive = False
        self.__start_nb = 0
        self.__thread = None
        self.__strict_timing = strict_timing
        return

    def start(self):
        """ Start Timer Object """
        self.__lock.acquire()
        try:
            if not self.__alive:
                self.debug('Timer::start()')
                self.__loop = True
                self.__alive = True
                self.__start_nb += 1
                thread_name = 'TimerLoop %d' % self.__start_nb
                self.__thread = threading.Thread(target=self.__run, name=thread_name)
                self.__thread.setDaemon(True)
                self.__thread.start()
        finally:
            self.__lock.release()

    def stop(self):
        """ Stop Timer Object """
        self.debug('Timer::stop()')
        self.__lock.acquire()
        self.__loop = False
        self.__lock.release()

    def __run(self):
        """ Private Thread Function """
        self.debug('Timer thread starting')
        next_time = time.time() + self.__interval
        while self.__loop:
            self.__function(*self.__args, **self.__kwargs)
            nap = self.__interval
            if self.__strict_timing:
                curr_time = time.time()
                nap = max(0, next_time - curr_time)
                if curr_time > next_time:
                    self.warning('loop function took more than loop interval (%ss)', self.__interval)
            next_time += self.__interval
            time.sleep(nap)

        self.__alive = False
        self.debug('Timer thread ending')