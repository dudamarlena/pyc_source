# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/horn/Code/pythonprojects/py_alg_dat/testsuite/test_association.py
# Compiled at: 2016-08-31 21:57:00
__doc__ = '\nTest of Association - a DTO class with key and value pair.\n'
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