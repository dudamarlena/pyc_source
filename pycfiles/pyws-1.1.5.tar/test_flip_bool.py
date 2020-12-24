# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_flip_bool.py
# Compiled at: 2013-08-11 10:36:51
from suds import null
import unittest2 as unittest
from testcases.base import BaseTestCaseMixin

class FlipBoolTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_null(self):
        self.assertEqual(self.service.flip_boolean(null()), True)

    def test_numeric(self):
        self.assertEqual(self.service.flip_boolean(0), True)

    def test_simple(self):
        self.assertEqual(self.service.flip_boolean(True), False)
        self.assertEqual(self.service.flip_boolean(False), True)