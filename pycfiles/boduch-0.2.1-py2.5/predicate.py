# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/test/predicate.py
# Compiled at: 2009-08-14 17:29:28
"""Unit tests for predicates."""
import unittest
from boduch.predicate import Predicate, Equal, Greater, Lesser
from boduch.interface import IPredicate

class TestPredicate(unittest.TestCase):

    def setUp(self):
        self.predicate_obj = Predicate(False, False)

    def test_A_interface(self):
        """Testing the Predicate interface"""
        self.assertTrue(IPredicate.implementedBy(Predicate), 'IPredicate not implemented by Predicate.')
        self.assertTrue(IPredicate.providedBy(self.predicate_obj), 'IPredicate not provided by Predicate instance.')

    def test_B_equal_true(self):
        """Testing the Equal predicate is true"""
        self.assertTrue(Equal(1, 1))

    def test_C_equal_false(self):
        """Testing the Equal predicate is false"""
        self.assertFalse(Equal(1, 2))

    def test_D_greater_true(self):
        """Testing the Greater predicate is true"""
        self.assertTrue(Greater(2, 1))

    def test_E_greater_false(self):
        """Testing the Greater predicate is false"""
        self.assertFalse(Greater(1, 2))

    def test_F_lesser_true(self):
        """Testing the Lesser predicate is true"""
        self.assertTrue(Lesser(1, 2))

    def test_G_lesser_false(self):
        """Testing the Lesser predicate is false"""
        self.assertFalse(Lesser(2, 1))


SuitePredicate = unittest.TestLoader().loadTestsFromTestCase(TestPredicate)
__all__ = [
 'TestPredicate', 'SuitePredicate']