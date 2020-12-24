# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_stop_fuse.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1465 bytes
import unittest, jittor as jt, numpy as np
from .test_core import expect_error

class TestStopFuse(unittest.TestCase):

    def test_stop_fuse(self):
        with jt.profile_scope() as (report):
            a = jt.float32(0).stop_fuse()
            c = jt.float32(0)
            bs = [c]
            for i in range(2000):
                b = jt.float32(i) * 2 * c
                bs.append(b)
                a += b

            a = a * 2
            dbs = jt.grad(a, bs)
            jt.sync(dbs + [a])
        for a in report[1:]:
            assert len(a[0].split('opkey')) < 50

    def test_stop_fuse2(self):
        with jt.profile_scope() as (report):
            a = jt.float32(0).stop_fuse()
            c = jt.float32(0).stop_fuse()
            bs = [c]
            for i in range(2000):
                b = jt.float32(i) * 2 * c
                bs.append(b)
                a += b

            a = a * 2
            dbs = jt.grad(a, bs)
            jt.sync(dbs + [a])
        for a in report[1:]:
            assert len(a[0].split('opkey')) < 8


if __name__ == '__main__':
    unittest.main()