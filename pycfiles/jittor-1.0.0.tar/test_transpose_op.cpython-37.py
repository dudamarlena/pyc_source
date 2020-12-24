# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_transpose_op.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 2497 bytes
import unittest, jittor as jt, numpy as np
from .test_core import expect_error
from .test_grad import ngrad
from itertools import permutations

def gen_data(shape):
    num = np.multiply.reduce(shape)
    a = np.arange(0, num)
    return a.reshape(shape)


class TestTransposeOp(unittest.TestCase):

    def test_with_np(self):

        def check(a):
            perms = list(permutations(range(a.ndim))) + [None]
            for perm in perms:
                if perm:
                    x = np.transpose(a, perm)
                    y = jt.transpose(a, perm).data
                else:
                    x = np.transpose(a)
                    y = jt.transpose(a).data
                self.assertEqual(x.shape, y.shape)
                assert (x == y).all(), f"\n{x}\n{y}"

        ia = [
         gen_data([2, 2, 2]), gen_data([2, 3, 4, 5]), gen_data([5, 3])]
        for a in ia:
            check(a)

    def test_grad(self):

        def check(a):
            perms = list(permutations(range(a.ndim))) + [None]
            for perm in perms:
                x = jt.array(a).float()
                if perm:
                    y = x.transpose(perm)
                else:
                    y = x.transpose()
                dx = jt.grad(y * y, x).data
                self.assertEqual(dx.shape, a.shape)
                assert (dx == a * 2).all(), f"\n{dx}\n{a}\n{perm}"

        ia = [
         gen_data([2, 2, 2]), gen_data([2, 3, 4, 5]), gen_data([5, 3])]
        for a in ia:
            check(a)

    def test_matmul_grad(self):
        np.random.seed(0)
        for i in range(10):
            a = np.random.rand(2, 3).astype('float32')
            b = np.random.rand(3, 4).astype('float32')
            out, (da, db) = ngrad(lambda vars: np.matmul(vars[0], vars[1]).sum(), [a, b], 0.1)
            ja = jt.array(a)
            jb = jt.array(b)
            jc = ja.matmul(jb)
            jda, jdb = jt.grad(jc, [ja, jb])
            assert (da - jda.data < 1e-05).all(), (da, jda.data, da - jda.data)
            assert (db - jdb.data < 1e-05).all(), db - jdb.data


if __name__ == '__main__':
    unittest.main()