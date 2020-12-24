# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/running/threadedrunner.py
# Compiled at: 2009-10-07 18:08:46
"""Run tests in multiple threads"""
from baserunner import BaseRunner

class ThreadedRunner(BaseRunner):
    """Run tests using a threadpool"""
    __module__ = __name__

    def __init__(self, num_threads):
        BaseRunner.__init__(self)
        from threadpool import ThreadPool
        self.pool = ThreadPool(num_threads)
        self.pool.start()

    def run(self, fixture):
        BaseRunner.run(self, fixture)
        self.pool.dispatch(fixture, self.reporter)

    def done(self):
        self.pool.stop()
        BaseRunner.done(self)