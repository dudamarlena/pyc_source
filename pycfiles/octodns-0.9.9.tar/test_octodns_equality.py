# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/test_octodns_equality.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals
from unittest import TestCase
from octodns.equality import EqualityTupleMixin

class TestEqualityTupleMixin(TestCase):

    def test_basics(self):

        class Simple(EqualityTupleMixin):

            def __init__(self, a, b, c):
                self.a = a
                self.b = b
                self.c = c

            def _equality_tuple(self):
                return (
                 self.a, self.b)

        one = Simple(1, 2, 3)
        same = Simple(1, 2, 3)
        matches = Simple(1, 2, b'ignored')
        doesnt = Simple(2, 3, 4)
        self.assertEquals(one, one)
        self.assertEquals(one, same)
        self.assertEquals(same, one)
        self.assertEquals(one, matches)
        self.assertEquals(matches, one)
        self.assertNotEquals(one, doesnt)
        self.assertNotEquals(doesnt, one)
        self.assertTrue(one < doesnt)
        self.assertFalse(doesnt < one)
        self.assertFalse(one < same)
        self.assertTrue(one <= doesnt)
        self.assertFalse(doesnt <= one)
        self.assertTrue(one <= same)
        self.assertFalse(one > doesnt)
        self.assertTrue(doesnt > one)
        self.assertFalse(one > same)
        self.assertFalse(one >= doesnt)
        self.assertTrue(doesnt >= one)
        self.assertTrue(one >= same)

    def test_not_implemented(self):

        class MissingMethod(EqualityTupleMixin):
            pass

        with self.assertRaises(NotImplementedError):
            MissingMethod() == MissingMethod()