# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_return_with_arguments_inside_generator.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 899 bytes
from sys import version_info
from pyflakes import messages as m
from pyflakes.test.harness import TestCase, skipIf

class Test(TestCase):

    @skipIf(version_info >= (3, 3), 'new in Python 3.3')
    def test_return(self):
        self.flakes('\n        class a:\n            def b():\n                for x in a.c:\n                    if x:\n                        yield x\n                return a\n        ', m.ReturnWithArgsInsideGenerator)

    @skipIf(version_info >= (3, 3), 'new in Python 3.3')
    def test_returnNone(self):
        self.flakes('\n        def a():\n            yield 12\n            return None\n        ', m.ReturnWithArgsInsideGenerator)

    @skipIf(version_info >= (3, 3), 'new in Python 3.3')
    def test_returnYieldExpression(self):
        self.flakes('\n        def a():\n            b = yield a\n            return b\n        ', m.ReturnWithArgsInsideGenerator)