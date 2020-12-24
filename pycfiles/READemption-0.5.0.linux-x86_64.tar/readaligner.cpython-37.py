# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/tests/readaligner.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 419 bytes
import unittest, sys
from io import StringIO
sys.path.append('.')
from reademptionlib.readmapper import ReadMapper

class TestReadMapper(unittest.TestCase):

    def setUp(self):
        self.read_mapper = ReadMapper('segemehl.x')

    @unittest.skip('TODO')
    def test_build_index(self):
        self.build_index()

    def test_run_mappings(self):
        pass


if __name__ == '__main__':
    unittest.main()