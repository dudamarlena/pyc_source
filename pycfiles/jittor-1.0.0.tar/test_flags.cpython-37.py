# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_flags.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1051 bytes
import unittest, jittor as jt
from .test_core import expect_error

class TestFlags(unittest.TestCase):

    def test_error(self):

        def check():
            jt.flags.asdasd = 1

        expect_error(check)

    def test_get_set(self):
        prev = jt.flags.log_v
        jt.flags.log_v = 1
        assert jt.flags.log_v == 1
        jt.flags.log_v = prev
        assert jt.flags.log_v == prev

    def test_scope(self):
        prev = jt.flags.log_v
        with jt.var_scope(log_v=1):
            assert jt.flags.log_v == 1
        assert jt.flags.log_v == prev

    def test_buildin(self):
        assert jt.flags.__doc__ == jt.core.flags.__doc__


if __name__ == '__main__':
    unittest.main()