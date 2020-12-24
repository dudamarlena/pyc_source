# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_classes.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 3806 bytes
"""Unit tests for the variables checker."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, astroid
from pylint.checkers import classes
from pylint.testutils import CheckerTestCase, Message, set_config

class TestVariablesChecker(CheckerTestCase):
    CHECKER_CLASS = classes.ClassChecker

    def test_bitbucket_issue_164(self):
        """Issue 164 report a false negative for access-member-before-definition"""
        n1, n2 = astroid.extract_node('\n        class MyClass1:\n          def __init__(self):\n            self.first += 5 #@\n            self.first = 0  #@\n        ')
        message = Message('access-member-before-definition',
          node=(n1.target), args=('first', n2.lineno))
        with self.assertAddsMessages(message):
            self.walk(n1.root())

    @set_config(exclude_protected=('_meta', '_manager'))
    def test_exclude_protected(self):
        """Test that exclude-protected can be used to
        exclude names from protected-access warning.
        """
        node = astroid.parse("\n        class Protected:\n            '''empty'''\n            def __init__(self):\n                self._meta = 42\n                self._manager = 24\n                self._teta = 29\n        OBJ = Protected()\n        OBJ._meta\n        OBJ._manager\n        OBJ._teta\n        ")
        with self.assertAddsMessages(Message('protected-access', node=(node.body[(-1)].value), args='_teta')):
            self.walk(node.root())

    def test_regression_non_parent_init_called_tracemalloc(self):
        node = astroid.extract_node('\n        from tracemalloc import Sequence\n        class _Traces(Sequence):\n            def __init__(self, traces): #@\n                Sequence.__init__(self)\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_super_init_not_called_regression(self):
        node = astroid.extract_node('\n        import ctypes\n\n        class Foo(ctypes.BigEndianStructure):\n            def __init__(self): #@\n                ctypes.BigEndianStructure.__init__(self)\n        ')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_uninferable_attribute(self):
        """Make sure protect-access doesn't raise
        an exception Uninferable attributes"""
        node = astroid.extract_node('\n        class MC():\n            @property\n            def nargs(self):\n                return 1 if self._nargs else 2\n\n        class Application(metaclass=MC):\n            def __new__(cls):\n                nargs = obj._nargs #@\n        ')
        with self.assertAddsMessages(Message('protected-access', node=(node.value), args='_nargs')):
            self.checker.visit_attribute(node.value)