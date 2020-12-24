# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/horn/Code/pythonprojects/py_alg_dat/testsuite/test_association.py
# Compiled at: 2016-08-31 21:57:00
"""
Test of Association - a DTO class with key and value pair.
"""
import unittest
from py_alg_dat import association

class TestAssociation(unittest.TestCase):
    """
    Test Association class.
    """

    def setUp(self):
        self.assoc1 = association.Association('k1', 1)
        self.assoc2 = association.Association('k2', 2)
        self.assoc3 = association.Association('k1', 1)

    def test_association_get_key(self):
        """
        Test get key method.
        """
        self.assertEqual('k1', self.assoc1.get_key())

    def test_association_get_value(self):
        """
        Test get value method.
        """
        self.assertEqual(1, self.assoc1.get_value())

    def test_association_equal(self):
        """
        Test equal operator.
        """
        self.assertEqual(self.assoc1, self.assoc3)

    def test_association_not_equal(self):
        """
        Test inequal operator.
        """
        self.assertNotEqual(self.assoc1, self.assoc2)