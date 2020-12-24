# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_add_integer_dicts.py
# Compiled at: 2013-08-11 10:36:51
from suds import null
import unittest2 as unittest
from testcases.base import BaseTestCaseMixin

class AddIntegerDictsTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_null_args(self):
        res = self.service.add_integer_dicts(null(), null())
        self.assertEqual(res.a, 0)
        self.assertEqual(res.b, 0)

    def test_null(self):
        p = self.factory.create('types:ABIntegerDict')
        p.a = null()
        p.b = null()
        q = self.factory.create('types:ABIntegerDict')
        q.a = null()
        q.b = null()
        res = self.service.add_integer_dicts(p, q)
        self.assertEqual(res.a, 0)
        self.assertEqual(res.b, 0)

    def test_empty(self):
        p = self.factory.create('types:ABIntegerDict')
        p.a = 0
        p.b = 0
        q = self.factory.create('types:ABIntegerDict')
        q.a = 0
        q.b = 0
        res = self.service.add_integer_dicts(p, q)
        self.assertEqual(res.a, 0)
        self.assertEqual(res.b, 0)

    def test_simple(self):
        p = self.factory.create('types:ABIntegerDict')
        p.a = 100
        p.b = 50
        q = self.factory.create('types:ABIntegerDict')
        q.a = 50
        q.b = 25
        res = self.service.add_integer_dicts(p, q)
        self.assertEqual(res.a, 150)
        self.assertEqual(res.b, 75)