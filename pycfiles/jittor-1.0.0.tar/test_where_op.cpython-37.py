# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_where_op.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1941 bytes
import unittest, jittor as jt, numpy as np

class TestWhereOp(unittest.TestCase):

    def test(self):
        if not (jt.where([0, 1, 0, 1])[0].data == [1, 3]).all():
            raise AssertionError
        else:
            a, = jt.where([0, 1, 0, 1])
            assert a.uncertain_shape == [-4]
            a.data
            assert a.uncertain_shape == [2]
            a, b = jt.where([[0, 0, 1], [1, 0, 0]])
            raise (a.data == [0, 1]).all() and (b.data == [2, 0]).all() or AssertionError

    def test_reindex_dep(self):
        a = jt.random([10])
        b, = (a > 1).where()
        assert len(b.data) == 0
        b, = (a > 0.5).where()
        assert (b.data == np.where(a.data > 0.5)).all()
        b = a.reindex_var((a > 0.5).where())
        assert (b.data == a.data[(a.data > 0.5)]).all()

    def test_binary_dep(self):
        a = jt.random([10])
        b, = (a > 0.5).where()
        b = b + 1
        assert (b.data == np.where(a.data > 0.5)[0] + 1).all()
        b, = (a > 1).where()
        b = b + 1
        assert (b.data == np.where(a.data > 1)[0] + 1).all()

    def test_self_dep(self):
        a = jt.random([100])
        x = a.reindex_var((a > 0.1).where())
        x = x.reindex_var((x < 0.9).where())
        na = a.data
        assert (na[np.logical_and(na > 0.1, na < 0.9)] == x.data).all()

    def test_reduce_dep(self):
        a = jt.random([100, 100])
        index = (a > 0.5).where()
        x = a.reindex_var(index)
        xsum = x.sum()
        na = a.data
        assert np.allclose(np.sum(na[(na > 0.5)]), xsum.data), (x.data, xsum.data, np.sum(na[(na > 0.5)]))

    def test_doc(self):
        assert 'Where Operator' in jt.where.__doc__


if __name__ == '__main__':
    unittest.main()