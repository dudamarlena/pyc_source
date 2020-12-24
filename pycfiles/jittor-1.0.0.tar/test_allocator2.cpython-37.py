# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_allocator2.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1519 bytes
import unittest, jittor as jt, gc

def test(h, w, total_alloc_call, total_alloc_byte, total_free_call=0, total_free_byte=0):
    jt.clean()
    jt.gc()
    with jt.flag_scope(use_stat_allocator=1):
        a = jt.random([h, w])
        b = a + a
        c = a * b
        c.data
        del a
        del b
        del c
        gc.collect()
        x = (
         jt.flags.stat_allocator_total_alloc_call,
         jt.flags.stat_allocator_total_alloc_byte,
         jt.flags.stat_allocator_total_free_call,
         jt.flags.stat_allocator_total_free_byte)
        y = (
         total_alloc_call, total_alloc_byte, total_free_call, total_free_byte)
        assert x == y, (x, y)


class TestAllocator2(unittest.TestCase):

    def test_stat(self):
        test(10, 10, 1, 1048576)
        test(100, 100, 1, 1048576)
        test(1000, 1000, 1, 20971520)
        test(8000, 1000, 2, 67108864)


if __name__ == '__main__':
    unittest.main()