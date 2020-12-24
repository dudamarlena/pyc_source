# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hstools/threads.py
# Compiled at: 2019-09-23 12:05:51
# Size of source mod 2**32: 1418 bytes
from __future__ import print_function
import time
from threading import Thread
from . import progress
from .compat import *

class threadWrapper(object):

    def __init__(self, func):
        self.func = func
        self.results = queue.Queue()

    def run(self, *args, **kwargs):
        self.thread = Thread(target=(self.f), args=args, kwargs=kwargs)
        self.thread.start()

    def f(self, *args, **kwargs):
        res = (self.func)(*args, **kwargs)
        self.results.put(res)

    def close(self):
        self.thread.join()

    def result(self):
        results = None
        if not self.results.empty():
            results = self.results.get()
        return results

    def isAlive(self):
        return self.thread.is_alive()

    def join(self):
        self.thread.join()


def runThreadedFunction(msg, success, func, *args, **kwargs):
    pbar = progress.progressBar(msg, type='dial', finish_message=success)
    threaded_func = threadWrapper(func)
    (threaded_func.run)(*args, **kwargs)
    while threaded_func.isAlive():
        time.sleep(0.2)
        pbar.writeprogress()

    threaded_func.join()
    pbar.success()
    res = threaded_func.result()
    return res