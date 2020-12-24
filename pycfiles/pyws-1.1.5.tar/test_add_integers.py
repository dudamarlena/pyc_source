# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_add_integers.py
# Compiled at: 2013-08-11 10:36:51
import unittest2 as unittest
from suds import null
from testcases.base import BaseTestCaseMixin

class AddIntegersTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_null(self):
        self.assertEqual(self.service.add_integers(null(), null()), 0)

    def test_empty(self):
        self.assertEqual(self.service.add_integers(0, 0), 0)

    def test_simple(self):
        self.assertEqual(self.service.add_integers(100, 50), 150)