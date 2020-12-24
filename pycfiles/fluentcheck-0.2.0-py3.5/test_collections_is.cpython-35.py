# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_is/test_collections_is.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 2730 bytes
import unittest
from fluentcheck import Is
from fluentcheck.exceptions import CheckError

class TestIsCollectionsAssertions(unittest.TestCase):

    def test_is_set_pass(self):
        obj = set()
        self.assertIsInstance(Is(obj).set, Is)

    def test_is_set_fail(self):
        with self.assertRaises(CheckError):
            Is(42).set

    def test_is_not_set_pass(self):
        self.assertIsInstance(Is(42).not_set, Is)

    def test_is_not_set_fail(self):
        obj = set()
        with self.assertRaises(CheckError):
            Is(obj).not_set

    def test_is_subset_of_pass(self):
        obj = {1, 2, 3}
        full_set = {1, 2, 3, 4, 5}
        self.assertIsInstance(Is(obj).subset_of(full_set), Is)

    def test_is_subset_of_fail(self):
        obj = {
         1, 2, 100}
        full_set = {1, 2, 3, 4, 5}
        with self.assertRaises(CheckError):
            Is(obj).subset_of(full_set)

    def test_is_not_subset_of_pass(self):
        obj = {1, 2, 3}
        full_set = {1, 7}
        self.assertIsInstance(Is(obj).not_subset_of(full_set), Is)

    def test_is_not_subset_of_fail(self):
        obj = {
         1, 2, 5}
        full_set = {1, 2, 3, 4, 5}
        with self.assertRaises(CheckError):
            Is(obj).not_subset_of(full_set)

    def test_is_superset_of_pass(self):
        obj = {1, 2, 3, 4, 5}
        subset = {1, 2, 3}
        self.assertIsInstance(Is(obj).superset_of(subset), Is)

    def test_is_superset_of_fail(self):
        obj = {
         1, 2, 3, 4, 5}
        subset = {1, 2, 100}
        with self.assertRaises(CheckError):
            Is(obj).superset_of(subset)

    def test_is_not_superset_of_pass(self):
        obj = {1, 2, 3, 4, 5}
        subset = {1, 100, 3}
        self.assertIsInstance(Is(obj).not_superset_of(subset), Is)

    def test_is_not_superset_of_fail(self):
        obj = {
         1, 2, 3, 4, 5}
        subset = {1, 2, 5}
        with self.assertRaises(CheckError):
            Is(obj).not_superset_of(subset)

    def test_is_intersects_pass(self):
        obj = {1, 2, 3, 4, 5}
        other_set = {1, 2, 3, 9, 100}
        self.assertIsInstance(Is(obj).intersects(other_set), Is)

    def test_is_intersects_fail(self):
        obj = {
         1, 2, 3, 4, 5}
        other_set = {-1, 100}
        with self.assertRaises(CheckError):
            Is(obj).intersects(other_set)

    def test_is_not_intersects_pass(self):
        obj = {1, 2, 3, 4, 5}
        other_set = {-1, 100}
        self.assertIsInstance(Is(obj).not_intersects(other_set), Is)

    def test_is_not_intersects_fail(self):
        obj = {
         1, 2, 3, 4, 5}
        other_set = {1, 2, 3, 9, 100}
        with self.assertRaises(CheckError):
            Is(obj).not_intersects(other_set)