# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_variables.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 8722 bytes
"""Unit tests for the variables checker."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, re, sys, astroid
from pylint.checkers import variables
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, Message, linter, set_config

class TestVariablesChecker(CheckerTestCase):
    CHECKER_CLASS = variables.VariablesChecker

    def test_bitbucket_issue_78(self):
        """ Issue 78 report a false positive for unused-module """
        module = astroid.parse("\n        from sys import path\n        path += ['stuff']\n        def func():\n            other = 1\n            return len(other)\n        ")
        with self.assertNoMessages():
            self.walk(module)

    @set_config(ignored_modules=('argparse', ))
    def test_no_name_in_module_skipped(self):
        """Make sure that 'from ... import ...' does not emit a
        'no-name-in-module' with a module that is configured
        to be ignored.
        """
        node = astroid.extract_node('\n        from argparse import THIS_does_not_EXIST\n        ')
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

    def test_all_elements_without_parent(self):
        node = astroid.extract_node('__all__ = []')
        node.value.elts.append(astroid.Const('test'))
        root = node.root()
        with self.assertNoMessages():
            self.checker.visit_module(root)
            self.checker.leave_module(root)

    def test_redefined_builtin_ignored(self):
        node = astroid.parse('\n        from future.builtins import open\n        ')
        with self.assertNoMessages():
            self.checker.visit_module(node)

    @set_config(redefining_builtins_modules=('os', ))
    def test_redefined_builtin_custom_modules(self):
        node = astroid.parse('\n        from os import open\n        ')
        with self.assertNoMessages():
            self.checker.visit_module(node)

    @set_config(redefining_builtins_modules=('os', ))
    def test_redefined_builtin_modname_not_ignored(self):
        node = astroid.parse('\n        from future.builtins import open\n        ')
        with self.assertAddsMessages(Message('redefined-builtin', node=(node.body[0]), args='open')):
            self.checker.visit_module(node)

    @set_config(redefining_builtins_modules=('os', ))
    def test_redefined_builtin_in_function(self):
        node = astroid.extract_node('\n        def test():\n            from os import open\n        ')
        with self.assertNoMessages():
            self.checker.visit_module(node.root())
            self.checker.visit_functiondef(node)

    def test_unassigned_global(self):
        node = astroid.extract_node('\n            def func():\n                global sys  #@\n                import sys, lala\n        ')
        msg = Message('global-statement', node=node, confidence=UNDEFINED)
        with self.assertAddsMessages(msg):
            self.checker.visit_global(node)


class TestVariablesCheckerWithTearDown(CheckerTestCase):
    CHECKER_CLASS = variables.VariablesChecker

    def setup_method(self):
        super(TestVariablesCheckerWithTearDown, self).setup_method()
        self._to_consume_backup = self.checker._to_consume
        self.checker._to_consume = []

    def teardown_method(self, method):
        self.checker._to_consume = self._to_consume_backup

    @set_config(callbacks=('callback_', '_callback'))
    def test_custom_callback_string(self):
        """ Test the --calbacks option works. """
        node = astroid.extract_node("\n        def callback_one(abc):\n             ''' should not emit unused-argument. '''\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)
        node = astroid.extract_node("\n        def two_callback(abc, defg):\n             ''' should not emit unused-argument. '''\n        ")
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)
        node = astroid.extract_node("\n        def normal_func(abc):\n             ''' should emit unused-argument. '''\n        ")
        with self.assertAddsMessages(Message('unused-argument', node=(node['abc']), args='abc')):
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)
        node = astroid.extract_node("\n        def cb_func(abc):\n             ''' Previous callbacks are overridden. '''\n        ")
        with self.assertAddsMessages(Message('unused-argument', node=(node['abc']), args='abc')):
            self.checker.visit_functiondef(node)
            self.checker.leave_functiondef(node)

    @set_config(redefining_builtins_modules=('os', ))
    def test_redefined_builtin_modname_not_ignored(self):
        node = astroid.parse('\n        from future.builtins import open\n        ')
        with self.assertAddsMessages(Message('redefined-builtin', node=(node.body[0]), args='open')):
            self.checker.visit_module(node)

    @set_config(redefining_builtins_modules=('os', ))
    def test_redefined_builtin_in_function(self):
        node = astroid.extract_node('\n        def test():\n            from os import open\n        ')
        with self.assertNoMessages():
            self.checker.visit_module(node.root())
            self.checker.visit_functiondef(node)

    def test_import_as_underscore(self):
        node = astroid.parse('\n        import math as _\n        ')
        with self.assertNoMessages():
            self.walk(node)

    def test_lambda_in_classdef(self):
        node = astroid.parse('\n        class MyObject(object):\n            method1 = lambda func: func()\n            method2 = lambda function: function()\n        ')
        with self.assertNoMessages():
            self.walk(node)

    def test_nested_lambda(self):
        """Make sure variables from parent lambdas
        aren't noted as undefined

        https://github.com/PyCQA/pylint/issues/760
        """
        node = astroid.parse('\n        lambda x: lambda: x + 1\n        ')
        with self.assertNoMessages():
            self.walk(node)

    @set_config(ignored_argument_names=(re.compile('arg')))
    def test_ignored_argument_names_no_message(self):
        """Make sure is_ignored_argument_names properly ignores
        function arguments"""
        node = astroid.parse('\n        def fooby(arg):\n            pass\n        ')
        with self.assertNoMessages():
            self.walk(node)

    @set_config(ignored_argument_names=(re.compile('args|kwargs')))
    def test_ignored_argument_names_starred_args(self):
        node = astroid.parse('\n        def fooby(*args, **kwargs):\n            pass\n        ')
        with self.assertNoMessages():
            self.walk(node)


class TestMissingSubmodule(CheckerTestCase):
    CHECKER_CLASS = variables.VariablesChecker

    def test_package_all(self):
        regr_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'regrtest_data')
        sys.path.insert(0, regr_data)
        try:
            linter.check(os.path.join(regr_data, 'package_all'))
            got = linter.reporter.finalize().strip()
            @py_assert2 = "E:  3: Undefined variable name 'missing' in __all__"
            @py_assert1 = got == @py_assert2
            if @py_assert1 is None:
                from _pytest.warning_types import PytestWarning
                from warnings import warn_explicit
                warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checker_variables.py', lineno=282)
            if not @py_assert1:
                @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (got, @py_assert2)) % {'py0':@pytest_ar._saferepr(got) if 'got' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(got) else 'got',  'py3':@pytest_ar._saferepr(@py_assert2)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert1 = @py_assert2 = None
        finally:
            sys.path.pop(0)