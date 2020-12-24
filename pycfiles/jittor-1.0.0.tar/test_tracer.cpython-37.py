# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_tracer.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 662 bytes
import unittest, jittor as jt

class TestTracer(unittest.TestCase):

    def test_print_trace(self):
        jt.print_trace()
        jt.flags.gdb_path = ''
        with jt.var_scope(gdb_path=''):
            jt.print_trace()


if __name__ == '__main__':
    unittest.main()