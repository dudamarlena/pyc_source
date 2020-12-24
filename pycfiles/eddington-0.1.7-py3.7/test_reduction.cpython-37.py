# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/input_data/test_reduction.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 5367 bytes
from collections import OrderedDict
from unittest import TestCase
from eddington.exceptions import ColumnsDuplicationError
from eddington.input.reduction import reduce_data

class ReducationBaseTestCase:
    data = OrderedDict([
     ('a', 1),
     ('b', 2),
     ('c', 3),
     ('d', 4),
     ('e', 5),
     ('f', 6),
     ('g', 7),
     ('h', 8),
     ('i', 9),
     ('k', 10)])

    def set_actual_items(self, reduced_data):
        self.actual_items = list(reduced_data.items())

    def test_length(self):
        self.assertEqual(4,
          (len(self.actual_items)),
          msg='Reduced data length is different than expected')

    def test_x(self):
        self.assertEqual((self.x),
          (self.actual_items[0]), msg='X is different than expected')

    def test_x_err(self):
        self.assertEqual((self.xerr),
          (self.actual_items[1]), msg='X error is different than expected')

    def test_y(self):
        self.assertEqual((self.y),
          (self.actual_items[2]), msg='Y is different than expected')

    def test_y_err(self):
        self.assertEqual((self.yerr),
          (self.actual_items[3]), msg='Y error is different than expected')


class TestReductionWithoutArgs(TestCase, ReducationBaseTestCase):
    x = ('a', 1)
    xerr = ('b', 2)
    y = ('c', 3)
    yerr = ('d', 4)

    def setUp(self):
        self.set_actual_items(reduce_data(self.data))


class TestReductionWithIntX(TestCase, ReducationBaseTestCase):
    x = ('c', 3)
    xerr = ('d', 4)
    y = ('e', 5)
    yerr = ('f', 6)

    def setUp(self):
        self.set_actual_items(reduce_data((self.data), x_column=3))


class TestReductionWithStringX(TestCase, ReducationBaseTestCase):
    x = ('c', 3)
    xerr = ('d', 4)
    y = ('e', 5)
    yerr = ('f', 6)

    def setUp(self):
        self.set_actual_items(reduce_data((self.data), x_column='c'))


class TestReductionWithIntY(TestCase, ReducationBaseTestCase):
    x = ('a', 1)
    xerr = ('b', 2)
    y = ('e', 5)
    yerr = ('f', 6)

    def setUp(self):
        self.set_actual_items(reduce_data((self.data), y_column=5))


class TestReductionWithStringY(TestCase, ReducationBaseTestCase):
    x = ('a', 1)
    xerr = ('b', 2)
    y = ('e', 5)
    yerr = ('f', 6)

    def setUp(self):
        self.set_actual_items(reduce_data((self.data), y_column='e'))


class TestReductionWithIntXerr(TestCase, ReducationBaseTestCase):
    x = ('a', 1)
    xerr = ('d', 4)
    y = ('e', 5)
    yerr = ('f', 6)

    def setUp(self):
        self.set_actual_items(reduce_data((self.data), xerr_column=4))


class TestReductionWithStringXerr(TestCase, ReducationBaseTestCase):
    x = ('a', 1)
    xerr = ('d', 4)
    y = ('e', 5)
    yerr = ('f', 6)

    def setUp(self):
        self.set_actual_items(reduce_data((self.data), xerr_column='d'))


class TestReductionWithIntYerr(TestCase, ReducationBaseTestCase):
    x = ('a', 1)
    xerr = ('b', 2)
    y = ('c', 3)
    yerr = ('f', 6)

    def setUp(self):
        self.set_actual_items(reduce_data((self.data), yerr_column=6))


class TestReductionWithStringYerr(TestCase, ReducationBaseTestCase):
    x = ('a', 1)
    xerr = ('b', 2)
    y = ('c', 3)
    yerr = ('f', 6)

    def setUp(self):
        self.set_actual_items(reduce_data((self.data), yerr_column='f'))


class TestReductionWithXAndY(TestCase, ReducationBaseTestCase):
    x = ('c', 3)
    xerr = ('d', 4)
    y = ('h', 8)
    yerr = ('i', 9)

    def setUp(self):
        self.set_actual_items(reduce_data((self.data), x_column=3, y_column='h'))


class TestReductionWithJumbledColumns(TestCase, ReducationBaseTestCase):
    x = ('c', 3)
    xerr = ('a', 1)
    y = ('b', 2)
    yerr = ('i', 9)

    def setUp(self):
        self.set_actual_items(reduce_data((self.data),
          x_column=3, xerr_column=1, y_column='b', yerr_column=9))


class TestReductionRaiseException(TestCase):
    data = OrderedDict([
     ('a', 1),
     ('b', 2),
     ('c', 3),
     ('d', 4),
     ('e', 5),
     ('f', 6),
     ('g', 7),
     ('h', 8),
     ('i', 9),
     ('k', 10)])

    def check(self):
        (self.assertRaisesRegex)(
         ColumnsDuplicationError, 
         (self.error_message), 
         reduce_data, 
         (self.data), **self.kwargs)

    def test_raise_exception_on_equal_x_and_xerr(self):
        self.error_message = '^All columns must be different. The following columns are the same: x, xerr$'
        self.kwargs = dict(x_column=1, xerr_column=1)
        self.check()

    def test_raise_exception_on_equal_x_and_y(self):
        self.error_message = '^All columns must be different. The following columns are the same: x, y$'
        self.kwargs = dict(x_column=1, y_column=1)
        self.check()

    def test_raise_exception_on_equal_x_xerr_and_y(self):
        self.error_message = '^All columns must be different. The following columns are the same: x, xerr, y$'
        self.kwargs = dict(x_column=2, xerr_column=2, y_column=2)
        self.check()