# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/input_data/test_extract_data_from_rows.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 3921 bytes
from collections import OrderedDict
from unittest import TestCase
import numpy as np
from eddington.exceptions import InvalidDataFile
from eddington.input.extraction import extract_data_from_rows

class ExtractDataFromRowsBaseTestSuite:
    file_name = 'name'
    decimal = 5

    def setUp(self):
        self.data = extract_data_from_rows(rows=(self.rows), file_name=(self.file_name))

    def test_type(self):
        self.assertEqual(OrderedDict,
          (type(self.data)), msg='Data type is different than expected')

    def test_headers(self):
        self.assertEqual((self.headers),
          (list(self.data.keys())),
          msg='Headers are different than expected')

    def test_items(self):
        for i, (expected_item, item) in enumerate(zip(self.items, self.data.items())):
            self.assertEqual((expected_item[0]),
              (item[0]), msg=f"Header {i} is different than expected")
            np.testing.assert_almost_equal((expected_item[1]),
              (item[1]),
              decimal=(self.decimal),
              err_msg=f"item {i} is different than expected")


class TestExtractDataFromRowsWithHeaders(TestCase, ExtractDataFromRowsBaseTestSuite):
    rows = [
     [
      'a', 'b', 'c', 'd'],
     [
      '1', '2', '3', '4'],
     [
      '5.1', '6.2', '7.3', '8.4'],
     [
      '-1', '-2', '-3', '-4']]
    headers = [
     'a', 'b', 'c', 'd']
    items = [
     (
      'a', [1, 5.1, -1]),
     (
      'b', [2, 6.2, -2]),
     (
      'c', [3, 7.3, -3]),
     (
      'd', [4, 8.4, -4])]

    def setUp(self):
        ExtractDataFromRowsBaseTestSuite.setUp(self)


class TestExtractDataFromRowsWithoutHeaders(TestCase, ExtractDataFromRowsBaseTestSuite):
    rows = [
     [
      '1', '2', '3', '4'],
     [
      '5.1', '6.2', '7.3', '8.4'],
     [
      '-1', '-2', '-3', '-4']]
    headers = [
     0, 1, 2, 3]
    items = [
     (
      0, [1, 5.1, -1]),
     (
      1, [2, 6.2, -2]),
     (
      2, [3, 7.3, -3]),
     (
      3, [4, 8.4, -4])]

    def setUp(self):
        ExtractDataFromRowsBaseTestSuite.setUp(self)


class ExtractDataFromRowsFailureBaseTestSuite:
    file_name = 'file_name'
    sheet = 'amazing sheet'

    def test_csv_raise_exception(self):
        self.assertRaisesRegex(InvalidDataFile,
          f'^"{self.file_name}" has invalid syntax.$',
          extract_data_from_rows,
          rows=(self.rows),
          file_name=(self.file_name))

    def test_excel_raise_exception(self):
        self.assertRaisesRegex(InvalidDataFile,
          f'^"{self.file_name}" has invalid syntax in sheet "{self.sheet}".$',
          extract_data_from_rows,
          rows=(self.rows),
          file_name=(self.file_name),
          sheet=(self.sheet))


class TestExtractDataFromRowsDataFailureWithNumberInHeaders(TestCase, ExtractDataFromRowsFailureBaseTestSuite):
    rows = [
     [
      'a', 'b', '5', 'd'],
     [
      '1', '2', '3', '4'],
     [
      '5.1', '6.2', '7.3', '8.4'],
     [
      '-1', '-2', '-3', '-4']]


class TestExtractDataFromRowsDataFailureWithEmptyInHeaders(TestCase, ExtractDataFromRowsFailureBaseTestSuite):
    rows = [
     [
      'a', 'b', '', 'd'],
     [
      '1', '2', '3', '4'],
     [
      '5.1', '6.2', '7.3', '8.4'],
     [
      '-1', '-2', '-3', '-4']]


class TestExtractDataFromRowsDataFailureWithoutHeadersWithStringInContent(TestCase, ExtractDataFromRowsFailureBaseTestSuite):
    rows = [
     [
      'a', 'b', 'c', 'd'],
     [
      '1', '2', '3', '4'],
     [
      '5.1', 'e', '7.3', '8.4'],
     [
      '-1', '-2', '-3', '-4']]


class TestExtractDataFromRowsDataFailureWithoutHeadersWithEmptyInContent(TestCase, ExtractDataFromRowsFailureBaseTestSuite):
    rows = [
     [
      'a', 'b', 'c', 'd'],
     [
      '1', '2', '3', '4'],
     [
      '5.1', '', '7.3', '8.4'],
     [
      '-1', '-2', '-3', '-4']]