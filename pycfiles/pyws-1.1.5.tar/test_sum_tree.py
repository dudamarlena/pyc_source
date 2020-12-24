# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stepank/projects/pyws/tests/python/suds/testcases/test_sum_tree.py
# Compiled at: 2013-08-11 10:36:51
import unittest2 as unittest
from testcases.base import BaseTestCaseMixin

class SumTreeTestCase(BaseTestCaseMixin, unittest.TestCase):

    def test_value(self):
        p = self.factory.create('types:Tree')
        p.value = 10
        p.left = None
        p.right = None
        self.assertEqual(self.service.sum_tree(p), 10)
        return

    def test_simple(self):
        p = self.factory.create('types:Tree')
        p.value = 10
        p.left = self.factory.create('types:Tree')
        p.left.value = 20
        p.left.left = None
        p.left.right = None
        p.right = self.factory.create('types:Tree')
        p.right.value = 30
        p.right.left = None
        p.right.right = None
        self.assertEqual(self.service.sum_tree(p), 60)
        return