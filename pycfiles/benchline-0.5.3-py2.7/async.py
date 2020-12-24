# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/async.py
# Compiled at: 2014-05-01 14:42:10
"""
Script to easily allow other python code to run
asynchronously.
"""
from functools import wraps
from multiprocessing import Process
from threading import Thread
import benchline.args

def threaded(func):
    """function decorator, intended to make "func" run in a separate
    thread (asynchronously).
    Returns the created Thread object

    E.g.:
    @threaded
    def task1():
        do_something

    t1 = task1()
    t1.join()
    """

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func


def forked(func):
    """function decorator, intended to make "func" run in a separate
    process (asynchronously).
    Returns the created Process object

    E.g.:
    @forked
    def process1():
        do_something

    p1 = process1()
    p1.join()
    """

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Process(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func


def main():
    benchline.args.go(__doc__, validate_args=None)
    return


if __name__ == '__main__':
    main()