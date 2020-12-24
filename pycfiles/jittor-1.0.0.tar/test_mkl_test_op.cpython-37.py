# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_mkl_test_op.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 623 bytes
import unittest, jittor as jt, os

@unittest.skipIf(not jt.compile_extern.use_mkl, 'Not use mkl, Skip')
class TestMklTestOp(unittest.TestCase):

    def test(self):
        assert jt.mkl_ops.mkl_test().data == 123


if __name__ == '__main__':
    unittest.main()