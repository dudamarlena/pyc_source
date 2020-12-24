# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/brent/anaconda/envs/fba/lib/python2.7/site-packages/examples/django_celery/demoapp/tests.py
# Compiled at: 2014-08-09 13:41:56
__doc__ = '\nThis file demonstrates writing tests using the unittest module. These will pass\nwhen you run "manage.py test".\n\nReplace this with more appropriate tests for your application.\n'
from django.test import TestCase

class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(2, 2)