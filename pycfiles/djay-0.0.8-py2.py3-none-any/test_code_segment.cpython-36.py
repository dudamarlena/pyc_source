# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_code_segment.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 4392 bytes
from pyflakes import messages as m
from pyflakes.checker import FunctionScope, ClassScope, ModuleScope, Argument, FunctionDefinition, Assignment
from pyflakes.test.harness import TestCase

class TestCodeSegments(TestCase):
    __doc__ = '\n    Tests for segments of a module\n    '

    def test_function_segment(self):
        self.flakes('\n        def foo():\n            def bar():\n                pass\n        ',
          is_segment=True)
        self.flakes('\n        def foo():\n            def bar():\n                x = 0\n        ',
          (m.UnusedVariable), is_segment=True)

    def test_class_segment(self):
        self.flakes('\n        class Foo:\n            class Bar:\n                pass\n        ',
          is_segment=True)
        self.flakes('\n        class Foo:\n            def bar():\n                x = 0\n        ',
          (m.UnusedVariable), is_segment=True)

    def test_scope_class(self):
        checker = self.flakes('\n        class Foo:\n            x = 0\n            def bar(a, b=1, *d, **e):\n                pass\n        ',
          is_segment=True)
        scopes = checker.deadScopes
        module_scopes = [scope for scope in scopes if scope.__class__ is ModuleScope]
        class_scopes = [scope for scope in scopes if scope.__class__ is ClassScope]
        function_scopes = [scope for scope in scopes if scope.__class__ is FunctionScope]
        self.assertEqual(len(module_scopes), 0)
        self.assertEqual(len(class_scopes), 1)
        self.assertEqual(len(function_scopes), 1)
        class_scope = class_scopes[0]
        function_scope = function_scopes[0]
        self.assertIsInstance(class_scope, ClassScope)
        self.assertIsInstance(function_scope, FunctionScope)
        self.assertIn('x', class_scope)
        self.assertIn('bar', class_scope)
        self.assertIn('a', function_scope)
        self.assertIn('b', function_scope)
        self.assertIn('d', function_scope)
        self.assertIn('e', function_scope)
        self.assertIsInstance(class_scope['bar'], FunctionDefinition)
        self.assertIsInstance(class_scope['x'], Assignment)
        self.assertIsInstance(function_scope['a'], Argument)
        self.assertIsInstance(function_scope['b'], Argument)
        self.assertIsInstance(function_scope['d'], Argument)
        self.assertIsInstance(function_scope['e'], Argument)

    def test_scope_function(self):
        checker = self.flakes('\n        def foo(a, b=1, *d, **e):\n            def bar(f, g=1, *h, **i):\n                pass\n        ',
          is_segment=True)
        scopes = checker.deadScopes
        module_scopes = [scope for scope in scopes if scope.__class__ is ModuleScope]
        function_scopes = [scope for scope in scopes if scope.__class__ is FunctionScope]
        self.assertEqual(len(module_scopes), 0)
        self.assertEqual(len(function_scopes), 2)
        function_scope_foo = function_scopes[1]
        function_scope_bar = function_scopes[0]
        self.assertIsInstance(function_scope_foo, FunctionScope)
        self.assertIsInstance(function_scope_bar, FunctionScope)
        self.assertIn('a', function_scope_foo)
        self.assertIn('b', function_scope_foo)
        self.assertIn('d', function_scope_foo)
        self.assertIn('e', function_scope_foo)
        self.assertIn('bar', function_scope_foo)
        self.assertIn('f', function_scope_bar)
        self.assertIn('g', function_scope_bar)
        self.assertIn('h', function_scope_bar)
        self.assertIn('i', function_scope_bar)
        self.assertIsInstance(function_scope_foo['bar'], FunctionDefinition)
        self.assertIsInstance(function_scope_foo['a'], Argument)
        self.assertIsInstance(function_scope_foo['b'], Argument)
        self.assertIsInstance(function_scope_foo['d'], Argument)
        self.assertIsInstance(function_scope_foo['e'], Argument)
        self.assertIsInstance(function_scope_bar['f'], Argument)
        self.assertIsInstance(function_scope_bar['g'], Argument)
        self.assertIsInstance(function_scope_bar['h'], Argument)
        self.assertIsInstance(function_scope_bar['i'], Argument)