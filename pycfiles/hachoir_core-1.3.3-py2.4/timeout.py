# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/timeout.py
# Compiled at: 2009-09-07 17:44:28
"""
limitedTime(): set a timeout in seconds when calling a function,
raise a Timeout error if time exceed.
"""
from math import ceil
IMPLEMENTATION = None

class Timeout(RuntimeError):
    """
    Timeout error, inherits from RuntimeError
    """
    __module__ = __name__


def signalHandler(signum, frame):
    """
    Signal handler to catch timeout signal: raise Timeout exception.
    """
    raise Timeout('Timeout exceed!')


def limitedTime(second, func, *args, **kw):
    """
    Call func(*args, **kw) with a timeout of second seconds.
    """
    return func(*args, **kw)


def fixTimeout(second):
    """
    Fix timeout value: convert to integer with a minimum of 1 second
    """
    if isinstance(second, float):
        second = int(ceil(second))
    assert isinstance(second, (int, long))
    return max(second, 1)


if not IMPLEMENTATION:
    try:
        from signal import signal, alarm, SIGALRM

        def limitedTime(second, func, *args, **kw):
            second = fixTimeout(second)
            old_alarm = signal(SIGALRM, signalHandler)
            try:
                alarm(second)
                return func(*args, **kw)
            finally:
                alarm(0)
                signal(SIGALRM, old_alarm)


        IMPLEMENTATION = 'signal.alarm()'
    except ImportError:
        pass

if not IMPLEMENTATION:
    try:
        from signal import signal, SIGXCPU
        from resource import getrlimit, setrlimit, RLIMIT_CPU

        def limitedTime(second, func, *args, **kw):
            second = fixTimeout(second)
            old_alarm = signal(SIGXCPU, signalHandler)
            current = getrlimit(RLIMIT_CPU)
            try:
                setrlimit(RLIMIT_CPU, (second, current[1]))
                return func(*args, **kw)
            finally:
                setrlimit(RLIMIT_CPU, current)
                signal(SIGXCPU, old_alarm)


        IMPLEMENTATION = 'resource.setrlimit(RLIMIT_CPU)'
    except ImportError:
        pass