# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_get_tree.py
# Compiled at: 2013-08-11 10:36:51
import unittest2 as unittest
from testcases.base import BaseTestCaseMixin

class GetTreeTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_none_ret(self):
        self.assertEqual(self.service.get_tree(0), None)
        return

    def test_notset(self):
        res = self.service.get_tree(1)
        self.assertEqual(res.value, 1)
        self.assertEqual(res.left, None)
        self.assertEqual(res.right, None)
        return

    def test_none(self):
        res = self.service.get_tree(2)
        self.assertEqual(res.value, 2)
        self.assertEqual(res.left, None)
        self.assertEqual(res.right, None)
        return

    def test_none_2(self):
        res = self.service.get_tree(3)
        self.assertEqual(res.value, 3)
        self.assertEqual(res.left.value, 4)
        self.assertEqual(res.left.left, None)
        self.assertEqual(res.left.right, None)
        self.assertEqual(res.right.value, 5)
        self.assertEqual(res.right.left, None)
        self.assertEqual(res.right.right, None)
        return