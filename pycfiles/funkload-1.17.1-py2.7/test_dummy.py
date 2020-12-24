# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/tests/test_dummy.py
# Compiled at: 2015-05-06 05:03:08
"""Dummy test used by test_Install.py

$Id$

simple doctest in a docstring:

  >>> 1 + 1
  2

"""
import unittest

class TestDummy1(unittest.TestCase):
    """Dummy test case."""

    def test_dummy1_1(self):
        self.assertEquals(2, 2)

    def test_dummy1_2(self):
        self.assertEquals(2, 2)


class TestDummy2(unittest.TestCase):
    """Dummy test case."""

    def test_dummy2_1(self):
        self.assertEquals(2, 2)

    def test_dummy2_2(self):
        self.assertEquals(2, 2)


class TestDummy3(unittest.TestCase):
    """Failing test case not part of the test_suite."""

    def test_dummy3_1(self):
        self.assertEquals(2, 2)

    def test_dummy3_2(self):
        self.assertEquals(2, 3, 'example of a failing test')

    def test_dummy3_3(self):
        impossible = 1 / 0
        self.assert_(2, 2)


class Dummy:
    """Testing docstring."""

    def __init__(self, value):
        self.value = value

    def double(self):
        """Return the double of the initial value.

        >>> d = Dummy(1)
        >>> d.double()
        2

        """
        return self.value * 2


def test_suite():
    """Return a test suite."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDummy1))
    suite.addTest(unittest.makeSuite(TestDummy2))
    return suite


if __name__ in ('main', '__main__'):
    unittest.main()