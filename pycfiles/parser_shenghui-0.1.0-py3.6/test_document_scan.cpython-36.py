# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/test_document_scan.py
# Compiled at: 2017-09-13 02:31:49
# Size of source mod 2**32: 1234 bytes
from parser import Parser
from .context import TEST_DATA_DIR_PATH
import unittest, os

class DocumentScanTestSuite(unittest.TestCase):
    __doc__ = 'Basic test cases.'

    def test_when_file_path_is_not_valid(self):
        parser = Parser()
        with self.assertRaises(Exception) as (context):
            parser.scan_document('myfile.txt')
        self.assertTrue('Could not open your document.' in str(context.exception))

    def test_when_file_path_is_correct_but_data_is_not_valid_value(self):
        parser = Parser()
        with self.assertRaises(Exception) as (context):
            file_path = os.path.join(TEST_DATA_DIR_PATH, 'bad_sample_value.txt')
            parser.scan_document(file_path)
        self.assertTrue('Your value is not a valid integer' in str(context.exception))

    def test_when_file_path_is_correct_but_data_is_not_valid_line(self):
        parser = Parser()
        with self.assertRaises(Exception) as (context):
            file_path = os.path.join(TEST_DATA_DIR_PATH, 'bad_sample_line.txt')
            parser.scan_document(file_path)
        self.assertTrue('Incorrect input line in document' in str(context.exception))


if __name__ == '__main__':
    unittest.main()