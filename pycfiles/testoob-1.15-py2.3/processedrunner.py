# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/running/processedrunner.py
# Compiled at: 2009-10-07 18:08:46
"""Run tests in processes"""
from baserunner import BaseRunner

class ProcessedRunner(BaseRunner):
    """Run tests using fork in different processes."""
    __module__ = __name__

    def __init__(self, max_processes=1):
        from processed_helper import ProcessedRunnerHelper
        BaseRunner.__init__(self)
        self._helper = ProcessedRunnerHelper(max_processes)

    def run(self, fixture):
        BaseRunner.run(self, fixture)
        self._helper.register_fixture(fixture)

    def done(self):
        self._helper.start(self.reporter)
        BaseRunner.done(self)