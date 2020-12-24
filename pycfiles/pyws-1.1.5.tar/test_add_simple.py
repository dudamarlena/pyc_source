# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_add_simple.py
# Compiled at: 2013-08-11 10:36:51
import unittest2 as unittest
from suds import null
from testcases.base import BaseTestCaseMixin

class AddSimpleTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_null(self):
        self.assertEqual(self.service.add_simple(null(), null()), None)
        return

    def test_empty(self):
        self.assertEqual(self.service.add_simple('', ''), None)
        return

    def test_simple(self):
        self.assertEqual(self.service.add_simple('hello', ' world'), 'hello world')

    def test_unicode(self):
        self.assertEqual(self.service.add_simple('hello', ' лопата'), 'hello лопата')