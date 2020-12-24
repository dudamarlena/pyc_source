# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_add_string_dicts.py
# Compiled at: 2013-08-11 10:36:51
from suds import null
import unittest2 as unittest
from testcases.base import BaseTestCaseMixin

class AddStringDictsTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_null_args(self):
        res = self.service.add_string_dicts(null(), null())
        self.assertEqual(res.a, None)
        self.assertEqual(res.b, None)
        return

    def test_null(self):
        p = self.factory.create('types:ABStringDict')
        p.a = null()
        p.b = null()
        q = self.factory.create('types:ABStringDict')
        q.a = null()
        q.b = null()
        res = self.service.add_string_dicts(p, q)
        self.assertEqual(res.a, None)
        self.assertEqual(res.b, None)
        return

    def test_empty(self):
        p = self.factory.create('types:ABStringDict')
        p.a = ''
        p.b = ''
        q = self.factory.create('types:ABStringDict')
        q.a = ''
        q.b = ''
        res = self.service.add_string_dicts(p, q)

    def test_simple(self):
        p = self.factory.create('types:ABStringDict')
        p.a = 'hello'
        p.b = 'say'
        q = self.factory.create('types:ABStringDict')
        q.a = ' world'
        q.b = ' hello'
        res = self.service.add_string_dicts(p, q)
        self.assertEqual(res.a, 'hello world')
        self.assertEqual(res.b, 'say hello')