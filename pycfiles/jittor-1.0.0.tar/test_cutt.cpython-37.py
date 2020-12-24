# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_cutt.py
# Compiled at: 2020-04-11 06:08:16
# Size of source mod 2**32: 881 bytes
import unittest, jittor as jt, numpy as np
from jittor import compile_extern
from .test_log import find_log_with_re
import copy
if compile_extern.has_cuda:
    from jittor.compile_extern import cutt_ops
else:
    cutt_ops = None

class TestCutt(unittest.TestCase):

    @unittest.skipIf(cutt_ops == None, 'Not use cutt, Skip')
    @jt.flag_scope(use_cuda=1)
    def test(self):
        t = cutt_ops.cutt_test('213')
        assert t.data == 123


if __name__ == '__main__':
    unittest.main()