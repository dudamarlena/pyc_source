# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pytest_board/testrunner.py
# Compiled at: 2018-12-29 09:42:38
# Size of source mod 2**32: 1073 bytes
from .plugin import JSONReporter
from .utils import flush_q
import pytest
from multiprocessing import Queue
from queue import Empty

class TestRunner(object):

    def __init__(self, q=None, timeout=60, before_run=None, on_completed=None):
        self.q = q or Queue()
        self.timeout = timeout
        self.before_run = before_run
        self.on_completed = on_completed
        self.status = 'idle'

    def notify(self, *args):
        self.q.put((*('requested', ), *args))

    def result(self):
        return self.reporter.report

    def _run_hook(self, hook, *args):
        if hook is not None:
            hook(*args)

    def run(self):
        while True:
            try:
                status, reason = self.q.get(timeout=(self.timeout))
                print('****** test_run', reason)
            except Empty:
                continue

            flush_q(self.q)
            self._run_hook(self.before_run)
            reporter = JSONReporter()
            pytest.main(plugins=[reporter])
            self._run_hook(self.on_completed, reporter.report)