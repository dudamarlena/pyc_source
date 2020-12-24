# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_add_string_lists.py
# Compiled at: 2013-08-11 10:36:51
import unittest2 as unittest
from testcases.base import BaseTestCaseMixin

class AddStringListsTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_empty(self):
        p = self.factory.create('types:StringList')
        p.item = []
        q = self.factory.create('types:StringList')
        q.item = []
        res = self.service.add_string_lists(p, q)

    def test_simple(self):
        p = self.factory.create('types:StringList')
        p.item = ['a', 'b', 'c']
        q = self.factory.create('types:StringList')
        q.item = ['d', 'e', 'f']
        res = self.service.add_string_lists(p, q)
        self.assertEqual(res.item, ['ad', 'be', 'cf'])

    def test_diff_size(self):
        p = self.factory.create('types:StringList')
        p.item = ['a', 'b', 'c']
        q = self.factory.create('types:StringList')
        q.item = ['d', 'e', 'f', 'g', 'h']
        res = self.service.add_string_lists(p, q)
        self.assertEqual(res.item, ['ad', 'be', 'cf', 'g', 'h'])