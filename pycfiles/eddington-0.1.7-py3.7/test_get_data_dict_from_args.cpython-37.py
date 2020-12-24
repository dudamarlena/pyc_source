# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/input_data/test_get_data_dict_from_args.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 2730 bytes
from argparse import Namespace
from unittest import TestCase
from mock import patch, DEFAULT
from eddington.input.get import get_data_dict_from_args

class TestGetDataDictFromArgs(TestCase):
    func = 'func'
    data = 'data'
    data2 = 'data2'

    def setUp(self):
        self.args = Namespace()
        self.random_data = None
        self.csv_data = None
        self.excel_data = None

    def check(self):
        args_copy = Namespace(**vars(self.args))
        args_copy.random_data = self.random_data
        args_copy.csv_data = self.csv_data
        args_copy.excel_data = self.excel_data
        actual_data = get_data_dict_from_args(self.func, args_copy)
        self.assertEqual(self.expected_data, actual_data)

    def test_returns_none(self):
        self.expected_data = None
        self.check()

    @patch('eddington.input.get.random_data')
    def test_returns_random(self, random_data):
        random_data.return_value = self.data
        self.random_data = True
        self.args.xmin = 1
        self.args.xmax = 8
        self.args.measurements = 25
        self.args.xsigma = 0.1
        self.args.ysigma = 0.2
        self.args.min_coeff = 0
        self.args.max_coeff = 10
        self.args.actual_a = [1, 1, 1]
        self.expected_data = self.data
        self.check()
        (random_data.assert_called_with)(func=self.func, **vars(self.args))

    @patch.multiple('eddington.input.get',
      read_data_from_excel=DEFAULT, reduce_data=DEFAULT)
    def test_returns_from_excel(self, read_data_from_excel, reduce_data):
        read_data_from_excel.return_value = self.data
        reduce_data.return_value = self.data2
        filename = 'filename'
        sheet = 'sheet'
        self.excel_data = [filename, sheet]
        self.args.x_column = 'x_column'
        self.args.xerr_column = 'xerr_column'
        self.args.y_column = 'y_column'
        self.args.yerr_column = 'yerr_column'
        self.expected_data = self.data2
        self.check()
        (reduce_data.assert_called_with)(data_dict=self.data, **vars(self.args))

    @patch.multiple('eddington.input.get',
      read_data_from_csv=DEFAULT, reduce_data=DEFAULT)
    def test_returns_from_csv(self, read_data_from_csv, reduce_data):
        read_data_from_csv.return_value = self.data
        reduce_data.return_value = self.data2
        filename = 'filename'
        self.csv_data = filename
        self.args.x_column = 'x_column'
        self.args.xerr_column = 'xerr_column'
        self.args.y_column = 'y_column'
        self.args.yerr_column = 'yerr_column'
        self.expected_data = self.data2
        self.check()
        (reduce_data.assert_called_with)(data_dict=self.data, **vars(self.args))