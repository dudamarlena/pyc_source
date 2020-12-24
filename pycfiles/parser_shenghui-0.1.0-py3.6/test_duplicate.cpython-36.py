# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/test_duplicate.py
# Compiled at: 2017-09-13 02:53:47
# Size of source mod 2**32: 648 bytes
from parser import Parser
from .context import TEST_DATA_DIR_PATH
import unittest, os

class DuplicateTestSuite(unittest.TestCase):
    __doc__ = 'Basic test cases.'

    def setUp(self):
        self.file_path = os.path.join(TEST_DATA_DIR_PATH, 'duplicates_sample.txt')
        self.parser = Parser()
        self.parser.scan_document(self.file_path)

    def test_when_duplicate_value_for_different_uuids(self):
        self.assertEqual(len(self.parser.x_largest(0)), 0)
        self.assertCountEqual(self.parser.x_largest(3), ['1426828058', '1426828028', '1426828037'])


if __name__ == '__main__':
    unittest.main()