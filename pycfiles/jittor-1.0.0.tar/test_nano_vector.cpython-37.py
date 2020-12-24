# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_nano_vector.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1392 bytes
import unittest, jittor as jt, time
from .test_core import expect_error

class TestNanoVector(unittest.TestCase):

    def test(self):
        nvector = jt.NanoVector
        nv = nvector()
        nv.append(1)
        nv.append(2)
        nv.append(3)
        nv.append(1099511627776)
        assert nv[3] == 1099511627776
        assert str(nv) == '[1,2,3,1099511627776,]'
        assert nv == [1, 2, 3, 1099511627776]
        expect_error(lambda : nv.append(1099511627776))
        assert len(nv) == 4, nv
        s = 0
        for a in nv:
            s += a

        assert s == 1099511627782
        s = max(nv)
        assert s == 1099511627776
        a, b, c, d = nv
        assert [a, b, c, d] == nv
        assert nv[(-1)] == 1099511627776
        assert nv[:2] == [1, 2]
        assert nv[:-2] == [1, 2]
        assert nv[::-1] == list(nv)[::-1], (list(nv)[::-1], nv[::-1])
        assert nvector([1, 2]) + nvector([3, 4]) == [1, 2, 3, 4]
        a = nvector([1, 2])
        a += [3, 4]
        assert a == [1, 2, 3, 4], a


if __name__ == '__main__':
    unittest.main()