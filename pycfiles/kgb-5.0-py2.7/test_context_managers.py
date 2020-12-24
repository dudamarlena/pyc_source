# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kgb/tests/test_context_managers.py
# Compiled at: 2020-04-10 23:22:42
from __future__ import unicode_literals
from kgb.contextmanagers import spy_on
from kgb.tests.base import MathClass, TestCase

class SpyOnTests(TestCase):
    """Unit tests for spies.contextmanagers.spy_on."""

    def test_spy_on(self):
        """Testing spy_on context manager"""
        obj = MathClass()
        with spy_on(obj.do_math):
            self.assertTrue(hasattr(obj.do_math, b'spy'))
            result = obj.do_math()
            self.assertEqual(result, 3)
        self.assertFalse(hasattr(obj.do_math, b'spy'))

    def test_expose_spy(self):
        """Testing spy_on exposes `spy` via context manager"""
        obj = MathClass()
        with spy_on(obj.do_math) as (spy):
            self.assertTrue(hasattr(obj.do_math, b'spy'))
            self.assertIs(obj.do_math.spy, spy)
            result = obj.do_math()
            self.assertEqual(result, 3)
        self.assertFalse(hasattr(obj.do_math, b'spy'))