# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_add_integer_lists.py
# Compiled at: 2013-08-11 10:36:51
import unittest2 as unittest
from testcases.base import BaseTestCaseMixin

class AddIntegerListsTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_empty(self):
        p = self.factory.create('types:IntegerList')
        p.item = []
        q = self.factory.create('types:IntegerList')
        q.item = []
        res = self.service.add_integer_lists(p, q)

    def test_simple(self):
        p = self.factory.create('types:IntegerList')
        p.item = [1, 2, 3]
        q = self.factory.create('types:IntegerList')
        q.item = [3, -5, 0]
        res = self.service.add_integer_lists(p, q)
        self.assertEqual(res.item, [4, -3, 3])

    def test_diff_size(self):
        p = self.factory.create('types:IntegerList')
        p.item = [1, 2, 3]
        q = self.factory.create('types:IntegerList')
        q.item = [3, -5, 0, 11, -5]
        res = self.service.add_integer_lists(p, q)
        self.assertEqual(res.item, [4, -3, 3, 11, -5])