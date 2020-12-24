# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_contrib.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 2377 bytes
import unittest, jittor as jt, numpy as np
from .test_core import expect_error

class TestContrib(unittest.TestCase):

    def test_concat(self):

        def check(shape, dim, n):
            num = np.prod(shape)
            arr1 = []
            arr2 = []
            for i in range(n):
                a = (np.array(range(num)) + i * num).reshape(shape)
                arr1.append(a)
                arr2.append(jt.array(a))

            x = np.concatenate(tuple(arr1), dim)
            y = jt.contrib.concat(arr2, dim)
            assert (x == y.data).all()

        check([2, 3, 4], 0, 2)
        check([2, 3, 4], 1, 3)
        check([2, 3, 4], 2, 4)
        check([2, 3, 4, 5], 0, 4)
        check([2, 3, 4, 5], 2, 4)
        check([2, 3, 4, 5], 3, 4)
        check([1], 0, 20)

    def test_slice(self):

        def check(shape, slices):
            x = jt.random(shape)
            a = x[slices].data
            b = x.data[slices]
            assert (a == b).all(), (a, b)
            y = x.numpy()
            v = jt.random(a.shape)
            x[slices] = v
            y[slices] = v.data
            assert (x.data == y).all()

        check([3], 1)
        check([3, 3, 3, 3], ([[0], [1]], slice(None), [1, 2], 1))
        check([3, 3, 3, 3], (slice(None), slice(None), slice(None), slice(None)))
        check([3, 3, 3, 3], ([0, 1], [0, 1], [0, 1], [0, 1]))
        check([3, 3, 3, 3], ([0, 1], -2, slice(None), [0, 1]))
        check([3, 3, 3, 3], ([0, 1], slice(1, 2, 2), [1, 2], 1))
        check([3, 3, 3, 3], ([0, 1], slice(None), [1, 2], 1))
        check([10, 10, 10, 10], (slice(1, None, 2), slice(-1, None, 2), [1, 2], -4))
        check([20], 0)
        check([20], 10)
        check([20], -10)
        check([10, 10, 10, 10], 1)
        check([10, 10, 10, 10], (1, slice(None), 2))
        check([10, 10, 10, 10], (-2, slice(None), 2, slice(1, 9, 2)))


if __name__ == '__main__':
    unittest.main()