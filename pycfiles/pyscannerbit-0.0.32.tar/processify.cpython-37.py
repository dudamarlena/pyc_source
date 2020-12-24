# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gmartine/pyscannerbit/pyscannerbit/processify.py
# Compiled at: 2020-03-04 01:47:30
# Size of source mod 2**32: 1902 bytes
"""Utility to run a function as a process

   Modified from: https://gist.github.com/schlamar/2311116
"""
import os, sys, signal, traceback
from functools import wraps
from multiprocessing import Process, Queue

def processify(func):
    """Decorator to run a function as a process.
    Be sure that every argument and the return value
    is *pickable*.
    The created process is joined, so the code does not
    run in parallel.
    """

    def process_func(q, *args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except Exception:
            ex_type, ex_value, tb = sys.exc_info()
            error = (ex_type, ex_value, ''.join(traceback.format_tb(tb)))
            ret = None
        else:
            error = None
        q.put((ret, error))

    process_func.__name__ = func.__name__ + 'processify_func'
    setattr(sys.modules[__name__], process_func.__name__, process_func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        q = Queue()
        p = Process(target=process_func, args=([q] + list(args)), kwargs=kwargs)
        try:
            p.start()
            ret, error = q.get()
            p.join()
        except KeyboardInterrupt:
            print('CTRL-C detected, killing scan subprocess...')
            os.kill(p.pid, signal.SIGKILL)
            quit()

        if error:
            ex_type, ex_value, tb_str = error
            message = '%s (in subprocess)\n%s' % (ex_value.args, tb_str)
            raise ex_type(message)
        return ret

    return wrapper


@processify
def test_function():
    return os.getpid()


@processify
def test_deadlock():
    return range(30000)


@processify
def test_exception():
    raise RuntimeError('xyz')