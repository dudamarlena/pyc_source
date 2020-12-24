# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\dask_io_loop.py
# Compiled at: 2018-08-27 17:21:06
import distributed
from tornado.ioloop import IOLoop
from threading import Thread
from distributed import Scheduler, Worker, Executor
import logging, atexit
distributed.core.logging.propagate = False
__ioloop__ = IOLoop()

class DaskLoop:

    def __init__(self):
        self.loop = __ioloop__
        self.t = Thread(target=self.loop.start)
        self.t.start()