# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/aa/time.py
# Compiled at: 2020-04-02 02:54:53
# Size of source mod 2**32: 1260 bytes
import time
from contextlib import ContextDecorator
from loguru import logger as log

class calc_run_time(ContextDecorator):

    def __init__(self, name='run_time', base_time=1e-06):
        self.name = name
        self.base_time = base_time

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        self.end = time.time()
        self.elapse = self.end - self.start
        if self.elapse > self.base_time:
            log.info(f"*** Processing time for {self.name} is: {self.elapse:.6f} seconds ***")


def exec_time(func):

    def new_func(*args, **args2):
        t1 = time.time()
        back = func(*args, **args2)
        t2 = time.time() - t1
        if t2 > 1e-05:
            log.info(f"{func.__name__} > take time: {t2:.6f}s")
        return back

    return new_func


def timestamp_str(n=0):
    return f"{10 ** n * time.time():.0f}"


def timestamp_int(n=0):
    return int(f"{10 ** n * time.time():.0f}")


def time_current(time_format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(time_format)


def timestamp_to_format(aa, time_format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(time_format, time.localtime(aa))