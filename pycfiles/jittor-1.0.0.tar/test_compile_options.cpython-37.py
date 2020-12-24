# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_compile_options.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1098 bytes
import unittest, jittor as jt, os
from .test_log import find_log_with_re
from .test_fused_op import retry

class TestCompileOptions(unittest.TestCase):

    def test(self):
        a = jt.array([1, 2, 3])
        a.sync()
        assert a.compile_options == {}
        a.compile_options = {'compile_shapes': 1}
        assert a.compile_options == {'compile_shapes': 1}
        b = a + a
        assert b.compile_options == {}
        with jt.var_scope(compile_options={'compile_shapes': 1}):
            c = a + b
        assert c.compile_options == {'compile_shapes': 1}
        with jt.profile_scope() as (report):
            c.sync()
        if not (len(report) == 2 and 'compile_shapes:1' in report[1][0]):
            raise AssertionError


if __name__ == '__main__':
    unittest.main()