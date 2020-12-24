# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/running/processed_helper.py
# Compiled at: 2009-10-07 18:08:46
"""Helper for processed running"""

class ProcessedRunnerHelper:
    """A helper class to make ProcessedRunner shorter and clearer."""
    __module__ = __name__

    def __init__(self, max_processes):
        self._fixturesList = [ [] for i in xrange(max_processes) ]
        self._load_balance_idx = 0

    def register_fixture(self, fixture):
        self._fixturesList[self._load_balance_idx].append(fixture)
        self._load_balance_idx = (self._load_balance_idx + 1) % len(self._fixturesList)

    def start(self, reporter):
        from os import fork, pipe, fdopen, waitpid
        from sys import exit
        children = []
        for processFixtures in self._fixturesList:
            pid = fork()
            if pid == 0:
                self._run_fixtures(processFixtures, reporter)
                exit()
            children.append(pid)

        for child in children:
            waitpid(child, 0)

    def _run_fixtures(self, fixtures, reporter):
        [ fixture(reporter) for fixture in fixtures ]