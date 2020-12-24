# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyogp/apps/web/django/pyogp_webbot/login/tests.py
# Compiled at: 2009-12-22 03:50:08
__doc__ = '\nThis file demonstrates two different styles of tests (one doctest and one\nunittest). These will both pass when you run "manage.py test".\n\nReplace these with more appropriate tests for your application.\n'
from django.test import TestCase

class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(2, 2)


__test__ = {'doctest': '\nAnother way to test that 1 + 1 is equal to 2.\n\n>>> 1 + 1 == 2\nTrue\n'}