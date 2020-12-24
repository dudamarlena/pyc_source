# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/util/test_temp.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 912 bytes
import os, sys, unittest
from drove.util import temp

class TestTemp(unittest.TestCase):

    def _mock_flush(*args, **kwargs):
        pass

    def test_temp_variable(self):
        """Testing util.temp.variables: basic behaviour"""
        with temp.variables({'sys.argv': ['test_value']}):
            assert sys.argv[0] == 'test_value'
        assert sys.argv[0] != 'test_value'
        with temp.variables({'sys.stdout': self._mock_flush}):
            assert sys.stdout == self._mock_flush
        with self.assertRaises(ValueError):
            with temp.variables({'fail': None}):
                pass

    def test_temp_directory(self):
        """Testing util.temp.directory: basic behaviour"""
        with temp.directory() as (tmp_dir):
            assert os.path.isdir(tmp_dir)
        assert not os.path.isdir(tmp_dir)