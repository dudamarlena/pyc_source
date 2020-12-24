# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_default_var.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1354 bytes
import sys, os, jittor as jt, unittest, time, numpy as np
from .test_reorder_tuner import simple_parser
from .test_log import find_log_with_re

class TestDefaultVar(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_default_var(self):
        a = jt.array((2, 3, 3), np.float32)
        b = a * 2.0
        assert str(b.dtype) == 'float32'
        b = a * 2
        assert str(b.dtype) == 'float32'
        a = jt.array((2, 3, 3), np.int32)
        b = a * 2.0
        assert str(b.dtype) == 'float32'
        b = a * 2
        assert str(b.dtype) == 'int32'
        a = jt.array((2, 3, 3), np.float64)
        b = a * 2.0
        assert str(b.dtype) == 'float64'
        b = a * 2
        assert str(b.dtype) == 'float64'
        a = jt.array((2, 3, 3), np.int64)
        b = a * 2.0
        assert str(b.dtype) == 'float64'
        b = a * 2
        assert str(b.dtype) == 'int64'


if __name__ == '__main__':
    unittest.main()