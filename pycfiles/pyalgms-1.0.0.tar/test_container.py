# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/horn/Code/pythonprojects/py_alg_dat/testsuite/test_container.py
# Compiled at: 2016-08-31 21:57:00
__doc__ = '\nTest of Container class - a general container data structure.\n'
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