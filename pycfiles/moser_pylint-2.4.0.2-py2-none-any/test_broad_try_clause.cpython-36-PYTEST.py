# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_broad_try_clause.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 1624 bytes
"""Tests for the pylint checker in :mod:`pylint.extensions.broad_try_clause
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os.path as osp, unittest
from pylint import checkers
from pylint.extensions.broad_try_clause import BroadTryClauseChecker
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter

class BroadTryClauseTestReporter(BaseReporter):

    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []


class BroadTryClauseTC(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(BroadTryClauseTestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(BroadTryClauseChecker(cls._linter))
        cls._linter.disable('I')

    def test_broad_try_clause_message(self):
        elif_test = osp.join(osp.dirname(osp.abspath(__file__)), 'data', 'broad_try_clause.py')
        self._linter.check([elif_test])
        msgs = self._linter.reporter.messages
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].symbol, 'too-many-try-statements')
        self.assertEqual(msgs[0].msg, 'try clause contains 2 statements, expected at most 1')
        self.assertEqual(msgs[0].line, 5)


if __name__ == '__main__':
    unittest.main()