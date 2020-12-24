# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/horn/Code/pythonprojects/py_alg_dat/testsuite/test_entry.py
# Compiled at: 2016-08-31 21:57:00
__doc__ = '\nTest of Entry class - a DTO holding information used in graph algorithms.\n'
import unittest
from py_alg_dat import entry

class TestEntry(unittest.TestCase):
    """
    Test of Entry class.
    """

    def setUp(self):
        self.elem1 = entry.Entry()
        self.elem2 = entry.Entry()
        self.elem3 = entry.Entry()
        self.elem3.discovered = True
        self.elem4 = entry.Entry()
        self.elem4.discovered = True
        self.elem4.distance = 100
        self.elem4.predecessor = 10

    def test_entry_equal(self):
        """
        Test of equal operator.
        """
        self.assertEqual(self.elem1, self.elem2)

    def test_entry_not_equal(self):
        """
        Test of inequal operator.
        """
        self.assertNotEqual(self.elem1, self.elem3)

    def test_entry_get_discovered(self):
        """
        Test of get_discovered method.
        """
        self.assertTrue(self.elem3.get_discovered())

    def test_entry_get_distance(self):
        """
        Test of get_distance method.
        """
        self.assertEqual(self.elem4.get_distance(), 100)

    def test_entry_get_predecessor(self):
        """
        Test of get_predecessor method.
        """
        self.assertEqual(self.elem4.get_predecessor(), 10)

    def test_entry_rich_comparison(self):
        """
        Test of rich comparison operators.
        """
        elem1 = entry.Entry()
        elem2 = entry.Entry()
        elem3 = entry.Entry()
        elem1.discovered = True
        elem1.distance = 10
        elem1.predecessor = 15
        elem2.discovered = False
        elem2.distance = 5
        elem2.predecessor = 3
        elem3.discovered = True
        elem3.distance = 7
        elem3.predecessor = 12
        ref = [
         elem2, elem3, elem1]
        rsorted = [elem1, elem2, elem3]
        rsorted = sorted(rsorted, key=lambda e: (e.discovered, e.distance, e.predecessor))
        self.assertEqual(ref, rsorted)