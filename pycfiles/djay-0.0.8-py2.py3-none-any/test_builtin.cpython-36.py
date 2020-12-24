# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_builtin.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 871 bytes
"""
Tests for detecting redefinition of builtins.
"""
from sys import version_info
from pyflakes import messages as m
from pyflakes.test.harness import TestCase, skipIf

class TestBuiltins(TestCase):

    def test_builtin_unbound_local(self):
        self.flakes('\n        def foo():\n            a = range(1, 10)\n            range = a\n            return range\n\n        foo()\n\n        print(range)\n        ', m.UndefinedLocal)

    def test_global_shadowing_builtin(self):
        self.flakes('\n        def f():\n            global range\n            range = None\n            print(range)\n\n        f()\n        ')

    @skipIf(version_info >= (3, ), 'not an UnboundLocalError in Python 3')
    def test_builtin_in_comprehension(self):
        self.flakes('\n        def f():\n            [range for range in range(1, 10)]\n\n        f()\n        ', m.UndefinedLocal)