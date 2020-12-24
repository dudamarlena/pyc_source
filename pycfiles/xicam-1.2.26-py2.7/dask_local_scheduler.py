# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\client\dask_local_scheduler.py
# Compiled at: 2018-08-27 17:21:06
from distributed import Scheduler, Worker, Executor
from pipeline import msg

class LocalScheduler:

    def __init__(self, dloop):
        """
          Create a local scheduler and worker to run commands
        """
        self.dloop = dloop
        self.loop = dloop.loop
        msg.logMessage('Starting scheduler', msg.INFO)
        msg.logMessage(self.dloop, msg.DEBUG)
        msg.logMessage(self.dloop.loop, msg.DEBUG)
        self.s = Scheduler('localhost', loop=self.dloop.loop)
        self.s.start(0)
        msg.logMessage('End scheduler', msg.INFO)
        msg.logMessage('Starting worker', msg.INFO)
        self.w = Worker(self.s.ip, self.s.port, ncores=1, loop=self.loop)
        self.w.start(0)
        self.addr = self.s.ip
        self.port = self.s.port

    def execute(self):
        msg.logMessage('Starting executor', msg.INFO)
        self.executor = Executor(('{0}:{1}').format(self.addr, self.port))
        msg.logMessage('executor..', msg.DEBUG)

    def close(self):
        self.s.close()