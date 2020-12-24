# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_comparetozero.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 1841 bytes
"""Tests for the pylint checker in :mod:`pylint.extensions.emptystring
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, os.path as osp, unittest
from pylint import checkers
from pylint.extensions.comparetozero import CompareToZeroChecker
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter

class CompareToZeroTestReporter(BaseReporter):

    def handle_message(self, msg):
        self.messages.append(msg)

    def on_set_current_module(self, module, filepath):
        self.messages = []


class CompareToZeroUsedTC(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(CompareToZeroTestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(CompareToZeroChecker(cls._linter))
        cls._linter.disable('I')

    def test_comparetozero_message(self):
        elif_test = osp.join(osp.dirname(osp.abspath(__file__)), 'data', 'compare_to_zero.py')
        self._linter.check([elif_test])
        msgs = self._linter.reporter.messages
        self.assertEqual(len(msgs), 4)
        for msg in msgs:
            self.assertEqual(msg.symbol, 'compare-to-zero')
            self.assertEqual(msg.msg, 'Avoid comparisons to zero')

        self.assertEqual(msgs[0].line, 6)
        self.assertEqual(msgs[1].line, 9)
        self.assertEqual(msgs[2].line, 12)
        self.assertEqual(msgs[3].line, 15)


if __name__ == '__main__':
    unittest.main()