# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/autoforms/tests.py
# Compiled at: 2012-07-06 10:27:01
from django.test import TestCase

class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(2, 2)


__test__ = {'doctest': '\nAnother way to test that 1 + 1 is equal to 2.\n\n>>> 1 + 1 == 2\nTrue\n'}