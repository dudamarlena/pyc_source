# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/running/simplerunner.py
# Compiled at: 2009-10-07 18:08:46
"""Simple runner"""
from baserunner import BaseRunner

class SimpleRunner(BaseRunner):
    """Simple runner, simply runs each test (what more do you need? :-)"""
    __module__ = __name__

    def run(self, fixture):
        BaseRunner.run(self, fixture)
        fixture(self.reporter)
        return not self.reporter.isFailed()