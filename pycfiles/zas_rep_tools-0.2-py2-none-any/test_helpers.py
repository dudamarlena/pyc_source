# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/utils/test_helpers.py
# Compiled at: 2018-08-04 08:32:08
from __future__ import print_function
import sys, threading
from time import sleep
try:
    import thread
except ImportError:
    import _thread as thread

try:
    range, _print = xrange, print

    def print(*args, **kwargs):
        flush = kwargs.pop('flush', False)
        _print(*args, **kwargs)
        if flush:
            kwargs.get('file', sys.stdout).flush()


except NameError:
    pass

def quit_function(fn_name):
    sys.stderr.flush()
    thread.interrupt_main()


def exit_after(s):
    """
    use as decorator to exit process if 
    function takes longer than s seconds
    """

    def outer(fn):

        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()

            return result

        return inner

    return outer