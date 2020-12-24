# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/horn/Code/pythonprojects/py_alg_dat/testsuite/test_container.py
# Compiled at: 2016-08-31 21:57:00
"""
Test of Container class - a general container data structure.
"""
import unittest
from py_alg_dat import container

class TestContainer(unittest.TestCase):
    """
    Test Container class.
    """

    def setUp(self):
        """
        Setup global test variables.
        """
        self.con1 = container.Container()

    def test_container_get_count(self):
        """
        Test get count method.
        """
        self.assertEqual(0, self.con1.get_count())

    def test_container_is_empty(self):
        """
        Test is empty method.
        """
        self.assertTrue(self.con1.is_empty())