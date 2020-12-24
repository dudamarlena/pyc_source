# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_allocator.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 992 bytes
import unittest, jittor as jt, gc

class TestAllocator(unittest.TestCase):

    def test_stat(self):
        jt.clean()
        with jt.flag_scope(use_stat_allocator=1, use_sfrl_allocator=0):
            a = jt.random([10, 10])
            b = a + a
            c = a * b
            c.data
            del a
            del b
            del c
            gc.collect()
        assert jt.flags.stat_allocator_total_alloc_call == 2
        assert jt.flags.stat_allocator_total_alloc_byte == 800
        assert jt.flags.stat_allocator_total_free_call == 2
        assert jt.flags.stat_allocator_total_free_byte == 800


if __name__ == '__main__':
    unittest.main()