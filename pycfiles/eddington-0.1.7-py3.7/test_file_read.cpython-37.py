# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/input_data/test_file_read.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 1783 bytes
from collections import namedtuple
from pathlib import Path
from unittest import TestCase
from mock import patch, mock_open
from eddington.input.csv import read_data_from_csv
from eddington.input.excel import read_data_from_excel
DummyCell = namedtuple('DummyCell', 'value')

class TestFileRead(TestCase):
    file_name = 'file'
    filepath = Path('path/to') / file_name
    sheet = 'sheet'
    rows = [['a', 'b', 'c'], ['c', 'd', 'e']]
    data = 'data'

    @patch('csv.reader')
    @patch('eddington.input.csv.extract_data_from_rows')
    def test_csv_read(self, extract_data_from_rows, reader):
        reader.return_value = self.rows
        extract_data_from_rows.return_value = self.data
        m_open = mock_open()
        with patch('eddington.input.csv.open', m_open):
            actual_data = read_data_from_csv(self.filepath)
        self.assertEqual((self.data), actual_data, msg='Data is different than expected')
        extract_data_from_rows.assert_called_with(rows=(self.rows),
          file_name=(self.file_name))

    @patch('xlrd.open_workbook')
    @patch('eddington.input.excel.extract_data_from_rows')
    def test_excel_read(self, extract_data_from_rows, open_workbook):
        sheet = open_workbook.return_value.sheet_by_name.return_value
        sheet.nrows = len(self.rows)
        sheet.row.side_effect = lambda i: [DummyCell(value=element) for element in self.rows[i]]
        extract_data_from_rows.return_value = self.data
        actual_data = read_data_from_excel(self.filepath, self.sheet)
        self.assertEqual((self.data), actual_data, msg='Data is different than expected')
        extract_data_from_rows.assert_called_with(rows=(self.rows),
          file_name=(self.file_name),
          sheet=(self.sheet))