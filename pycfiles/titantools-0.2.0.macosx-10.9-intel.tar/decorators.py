# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/titantools/decorators.py
# Compiled at: 2014-06-19 12:52:07
"""
This is the declaration file for a set of useful decorators.
"""
from time import strftime, gmtime, time

def run_every_n_minutes(n_minutes, func):
    """
    a decorator for running functions every n minutes
    """

    def decorated(*args, **kwargs):
        """
        internal decorator method
        """
        minute = int(strftime('%M', gmtime()))
        ret = None
        if minute % n_minutes == 0:
            ret = func(*args, **kwargs)
        return ret

    return decorated


def run_every_5(func):
    """
    a decorator for running functions every 5 minutes
    """
    return run_every_n_minutes(5, func)


def run_every_10(func):
    """
    a decorator for running functions every 10 minutes
    """
    return run_every_n_minutes(10, func)


def run_every_15(func):
    """
    a decorator for running functions every 15 minutes
    """
    return run_every_n_minutes(15, func)


def run_every_20(func):
    """
    a decorator for running functions every 20 minutes
    """
    return run_every_n_minutes(20, func)


def run_every_30(func):
    """
    a decorator for running functions every 30 minutes
    """
    return run_every_n_minutes(30, func)


def run_every_60(func):
    """
    a decorator for running functions every 60 minutes
    """
    return run_every_n_minutes(60, func)


def timer(func):
    """
    a decorator for timing code execution
    """

    def decorated(*args, **kwargs):
        """
        internal decorator method
        """
        start = time()
        ret = func(*args, **kwargs)
        end = time()
        print 'ty_name=perf function="%s" time="%.4f"' % (
         func.__name__,
         end - start)
        return ret

    return decorated