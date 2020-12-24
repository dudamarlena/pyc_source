# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_exceptions.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 1795 bytes
"""Tests for pylint.checkers.exceptions."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, astroid
from pylint.checkers import exceptions
from pylint.testutils import CheckerTestCase, Message

class TestExceptionsChecker(CheckerTestCase):
    __doc__ = 'Tests for pylint.checkers.exceptions.'
    CHECKER_CLASS = exceptions.ExceptionsChecker

    def test_raising_bad_type_python3(self):
        node = astroid.extract_node('raise (ZeroDivisionError, None)  #@')
        message = Message('raising-bad-type', node=node, args='tuple')
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)

    def test_bad_exception_context_function(self):
        node = astroid.extract_node('\n        def function():\n            pass\n\n        try:\n            pass\n        except function as exc:\n            raise Exception from exc  #@\n        ')
        message = Message('bad-exception-context', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)