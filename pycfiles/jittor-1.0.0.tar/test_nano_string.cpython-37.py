# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_nano_string.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1174 bytes
import unittest, jittor as jt, time
from .test_core import expect_error
import os
mid = 0
if os.uname()[1] == 'jittor-ce':
    mid = 1

class TestNanoString(unittest.TestCase):

    def test(self):
        dtype = jt.NanoString
        t = time.time()
        n = 1000000
        for i in range(n):
            dtype('float')

        t = (time.time() - t) / n
        assert t < [1.5e-07, 1.7e-07][mid], t
        assert jt.hash('asdasd') == 4152566416
        assert str(jt.NanoString('float')) == 'float'


if __name__ == '__main__':
    unittest.main()