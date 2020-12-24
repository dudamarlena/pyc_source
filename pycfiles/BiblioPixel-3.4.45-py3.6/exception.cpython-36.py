# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/exception.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 604 bytes
import contextlib, traceback

@contextlib.contextmanager
def add(*args):
    """
    A context manager that appends arguments to any exception thrown

    :param args: Arguments to be appended to the ``.args`` attribute of any
                 exception that is thrown while the context manager is active
    """
    try:
        yield
    except Exception as e:
        e.args = args + e.args
        raise


def report(function, *args, **kwds):
    """Run a function, catch, report and discard exceptions"""
    try:
        function(*args, **kwds)
    except Exception:
        traceback.print_exc()