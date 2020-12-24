# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_logging.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 4977 bytes
"""Unittest for the logging checker."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, astroid
from pylint.checkers import logging
from pylint.testutils import CheckerTestCase, Message, set_config

class TestLoggingModuleDetection(CheckerTestCase):
    CHECKER_CLASS = logging.LoggingChecker

    def test_detects_standard_logging_module(self):
        stmts = astroid.extract_node("\n        import logging #@\n        logging.warn('%s' % '%s')  #@\n        ")
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(Message('logging-not-lazy', node=(stmts[1]))):
            self.checker.visit_call(stmts[1])

    def test_dont_crash_on_invalid_format_string(self):
        node = astroid.parse("\n        import logging\n        logging.error('0} - {1}'.format(1, 2))\n        ")
        self.walk(node)

    def test_detects_renamed_standard_logging_module(self):
        stmts = astroid.extract_node("\n        import logging as blogging #@\n        blogging.warn('%s' % '%s')  #@\n        ")
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(Message('logging-not-lazy', node=(stmts[1]))):
            self.checker.visit_call(stmts[1])

    @set_config(logging_modules=['logging', 'my.logging'])
    def test_nonstandard_logging_module(self):
        stmts = astroid.extract_node("\n        from my import logging as blogging #@\n        blogging.warn('%s' % '%s')  #@\n        ")
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(Message('logging-not-lazy', node=(stmts[1]))):
            self.checker.visit_call(stmts[1])

    def _assert_brace_format_no_messages(self, stmt):
        stmts = astroid.extract_node('\n        import logging #@\n        logging.error<placeholder> #@\n        '.replace('<placeholder>', stmt))
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertNoMessages():
            self.checker.visit_call(stmts[1])

    def _assert_brace_format_message(self, msg, stmt):
        stmts = astroid.extract_node('\n        import logging #@\n        logging.error<placeholder> #@\n        '.replace('<placeholder>', stmt))
        self.checker.visit_module(None)
        self.checker.visit_import(stmts[0])
        with self.assertAddsMessages(Message(msg, node=(stmts[1]))):
            self.checker.visit_call(stmts[1])

    def _assert_brace_format_too_few_args(self, stmt):
        self._assert_brace_format_message('logging-too-few-args', stmt)

    def _assert_brace_format_too_many_args(self, stmt):
        self._assert_brace_format_message('logging-too-many-args', stmt)

    @set_config(logging_format_style='new')
    def test_brace_format_style_matching_arguments(self):
        self._assert_brace_format_no_messages("('constant string')")
        self._assert_brace_format_no_messages("('{}')")
        self._assert_brace_format_no_messages("('{}', 1)")
        self._assert_brace_format_no_messages("('{0}', 1)")
        self._assert_brace_format_no_messages("('{named}', {'named': 1})")
        self._assert_brace_format_no_messages("('{} {named}', 1, {'named': 1})")
        self._assert_brace_format_no_messages("('{0} {named}', 1, {'named': 1})")

    @set_config(logging_format_style='new')
    def test_brace_format_style_too_few_args(self):
        self._assert_brace_format_too_few_args("('{}, {}', 1)")
        self._assert_brace_format_too_few_args("('{0}, {1}', 1)")
        self._assert_brace_format_too_few_args("('{named1}, {named2}', {'named1': 1})")
        self._assert_brace_format_too_few_args("('{0}, {named}', 1)")
        self._assert_brace_format_too_few_args("('{}, {named}', {'named': 1})")
        self._assert_brace_format_too_few_args("('{0}, {named}', {'named': 1})")

    @set_config(logging_format_style='new')
    def test_brace_format_style_not_enough_arguments(self):
        self._assert_brace_format_too_many_args("('constant string', 1, 2)")
        self._assert_brace_format_too_many_args("('{}', 1, 2)")
        self._assert_brace_format_too_many_args("('{0}', 1, 2)")
        self._assert_brace_format_too_many_args("('{}, {named}', 1, 2, {'named': 1})")
        self._assert_brace_format_too_many_args("('{0}, {named}', 1, 2, {'named': 1})")