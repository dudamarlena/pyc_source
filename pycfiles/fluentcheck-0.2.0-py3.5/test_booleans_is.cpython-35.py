# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_is/test_booleans_is.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 4085 bytes
import unittest
from fluentcheck import Is
from fluentcheck.exceptions import CheckError
from fluentcheck.tests.tests_check.test_booleans import BooleanByLengthObject, BooleanObject

class TestIsBooleansAssertions(unittest.TestCase):

    def setUp(self):
        self.falsy_values = ([], (), {}, set(), '', '',
         range(0), 0, 0.0, complex(0.0, 0.0), None, False,
         BooleanObject(False), BooleanByLengthObject())
        self.truthy_values = ([1], ('a', ), {1: 'one'}, {1, 1}, '1', '2',
         range(1), 1, 1.0, complex(0.0, 1.0), not None, True,
         BooleanObject(True), BooleanByLengthObject([1, 2]))

    def test_is_boolean_pass(self):
        self.assertIsInstance(Is(1 == 2).boolean, Is)

    def test_is_boolean_fail(self):
        with self.assertRaises(CheckError):
            Is(42).boolean

    def test_is_not_boolean_pass(self):
        obj = object()
        self.assertIsInstance(Is(obj).not_boolean, Is)

    def test_is_not_boolean_fail(self):
        with self.assertRaises(CheckError):
            Is(False).not_boolean

    def test_is_true_pass(self):
        self.assertIsInstance(Is(True).true, Is)

    def test_is_true_fail(self):
        with self.assertRaises(CheckError):
            Is(False).true

    def test_is_not_true_pass(self):
        self.assertIsInstance(Is(False).not_true, Is)

    def test_is_not_true_fail(self):
        with self.assertRaises(CheckError):
            Is(True).not_true

    def test_is_false_pass(self):
        self.assertIsInstance(Is(False).false, Is)

    def test_is_false_fail(self):
        with self.assertRaises(CheckError):
            Is(True).false

    def test_is_not_false_pass(self):
        self.assertIsInstance(Is(True).not_false, Is)

    def test_is_not_false_fail(self):
        with self.assertRaises(CheckError):
            Is(False).not_false

    def test_is_falsy_pass(self):
        self.assertIsInstance(Is([]).falsy, Is)

    def test_is_falsy_fail(self):
        obj = 'I am not falsy!'
        with self.assertRaises(CheckError):
            Is(obj).falsy

    def test_is_not_falsy_pass(self):
        for item in self.falsy_values:
            obj = not item
            self.assertIsInstance(Is(obj).not_falsy, Is)

    def test_is_not_falsy_fail(self):
        for item in self.falsy_values:
            obj = item
            try:
                Is(obj).not_falsy
                self.fail()
            except CheckError:
                pass

    def test_is_truthy_pass(self):
        for item in self.truthy_values:
            obj = item
            self.assertIsInstance(Is(obj).truthy, Is)

    def test_is_truthy_fail(self):
        for item in self.truthy_values:
            obj = not item
            try:
                Is(obj).truthy
                self.fail()
            except CheckError:
                pass

    def test_is_not_truthy_pass(self):
        for item in self.truthy_values:
            obj = not item
            self.assertIsInstance(Is(obj).not_truthy, Is)

    def test_is_not_truthy_fail(self):
        for item in self.truthy_values:
            obj = item
            try:
                Is(obj).not_truthy
                self.fail()
            except CheckError:
                pass

    def test_is_has_same_truth_of_pass(self):
        obj = BooleanObject(True)
        self.assertIsInstance(Is(obj).has_same_truth_of(BooleanByLengthObject([1, 2])), Is)

    def test_is_has_same_truth_of_fail(self):
        obj = BooleanObject(False)
        with self.assertRaises(CheckError):
            Is(obj).has_same_truth_of(BooleanByLengthObject([1, 2]))

    def test_is_has_opposite_truth_of_pass(self):
        obj = BooleanObject(False)
        self.assertIsInstance(Is(obj).has_opposite_truth_of(BooleanByLengthObject([1])), Is)

    def test_is_has_opposite_truth_of_fail(self):
        obj = BooleanObject(False)
        with self.assertRaises(CheckError):
            Is(obj).has_opposite_truth_of(BooleanByLengthObject())