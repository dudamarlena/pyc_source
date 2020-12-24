# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/core/pool_provider.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 1269 bytes
"""
This module allow us to simplify the logic of any method that can run with either multiple threads or single thread.

To use this wrapper with multiple threads::
    pool = pool_provider.get_pool()
    try:
        pool.map(function, iterable)
    finally:
        pool.terminate()

To use this wrapper for single thread, change the synapseclient.config.single_threaded::
    synapseclient.config.single_threaded = True

"""
import multiprocessing, multiprocessing.dummy
from . import config
DEFAULT_POOL_SIZE = 8

class SingleThreadPool:

    def map(self, func, iterable):
        for item in iterable:
            func(item)

    def terminate(self):
        pass


class FakeLock:

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass


class SingleValue:
    value = None

    def __init__(self, type, value):
        self.value = value

    def get_lock(self):
        return FakeLock()


def get_pool():
    if config.single_threaded:
        return SingleThreadPool()
    else:
        return multiprocessing.dummy.Pool(DEFAULT_POOL_SIZE)


def get_value(type, value):
    if config.single_threaded:
        return SingleValue(type, value)
    else:
        return multiprocessing.Value(type, value)