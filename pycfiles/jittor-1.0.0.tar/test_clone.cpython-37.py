# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_clone.py
# Compiled at: 2020-04-11 06:08:16
# Size of source mod 2**32: 775 bytes
import unittest, jittor as jt, numpy as np

class TestClone(unittest.TestCase):

    def test(self):
        jt.clean()
        b = a = jt.array(1)
        for i in range(10):
            b = b.clone()
            if i == 5:
                c = b

        b.sync()
        assert jt.number_of_lived_vars() == 11
        c.stop_grad()
        assert jt.number_of_lived_vars() == 3


if __name__ == '__main__':
    unittest.main()