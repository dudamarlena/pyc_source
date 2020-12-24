# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_is/test_sequences_is.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 2721 bytes
import unittest
from fluentcheck import Is
from fluentcheck.exceptions import CheckError

class TestIsSequencesAssertions(unittest.TestCase):

    def test_is_empty_pass(self):
        obj = []
        self.assertIsInstance(Is(obj).empty, Is)

    def test_is_empty_fail(self):
        obj = [
         1, 2]
        with self.assertRaises(CheckError):
            Is(obj).empty

    def test_is_not_empty_pass(self):
        obj = [1, 2]
        self.assertIsInstance(Is(obj).not_empty, Is)

    def test_is_not_empty_fail(self):
        obj = []
        with self.assertRaises(CheckError):
            Is(obj).not_empty

    def test_is_iterable_pass(self):
        obj = [1, 2]
        self.assertIsInstance(Is(obj).iterable, Is)

    def test_is_iterable_fail(self):
        obj = object()
        with self.assertRaises(CheckError):
            Is(obj).iterable

    def test_is_not_iterable_pass(self):
        obj = object()
        self.assertIsInstance(Is(obj).not_iterable, Is)

    def test_is_not_iterable_fail(self):
        obj = [
         1, 2]
        with self.assertRaises(CheckError):
            Is(obj).not_iterable

    def test_is_couple_pass(self):
        obj = (1, 2)
        self.assertIsInstance(Is(obj).couple, Is)

    def test_is_couple_fail(self):
        obj = (1, 2, 3)
        with self.assertRaises(CheckError):
            Is(obj).couple

    def test_is_triplet_pass(self):
        obj = (1, 2, 3)
        self.assertIsInstance(Is(obj).triplet, Is)

    def test_is_triplet_fail(self):
        obj = (1, 2, 3, 4, 5)
        with self.assertRaises(CheckError):
            Is(obj).triplet

    def test_is_nuple_pass(self):
        obj = (1, 2, 3, 4, 5)
        self.assertIsInstance(Is(obj).nuple(5), Is)

    def test_is_nuple_fail(self):
        obj = (1, 2, 3, 4, 5)
        with self.assertRaises(CheckError):
            Is(obj).nuple(3)

    def test_has_dimensionality_pass(self):
        obj = [[1, 2], [3, 4]]
        self.assertIsInstance(Is(obj).has_dimensionality(2), Is)

    def test_has_dimensionality_fail(self):
        obj = [
         [
          1, 2], [3, 4]]
        with self.assertRaises(CheckError):
            Is(obj).has_dimensionality(3)

    def test_is_tuple_pass(self):
        obj = (1, 2)
        self.assertIsInstance(Is(obj).tuple, Is)

    def test_is_tuple_fail(self):
        obj = [
         1, 2]
        with self.assertRaises(CheckError):
            Is(obj).tuple

    def test_is_list_pass(self):
        obj = [1, 2]
        self.assertIsInstance(Is(obj).list, Is)

    def test_is_list_fail(self):
        obj = (1, 2)
        with self.assertRaises(CheckError):
            Is(obj).list