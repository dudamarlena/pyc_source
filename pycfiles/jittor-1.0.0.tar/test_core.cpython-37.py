# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_core.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 2734 bytes
import unittest, jittor as jt, numpy as np

def expect_error(func):
    try:
        func()
    except Exception as e:
        try:
            return
        finally:
            e = None
            del e

    raise Exception('Expect an error, but nothing catched.')


class TestCore(unittest.TestCase):

    def test_number_of_hold_vars(self):
        assert jt.random([1, 2, 3]).peek() == 'float[1,2,3,]'
        assert jt.core.number_of_hold_vars() == 0
        x = jt.random([1, 2, 3])
        assert jt.core.number_of_hold_vars() == 1
        del x
        assert jt.core.number_of_hold_vars() == 0

    def test_fetch_sync(self):
        dtypes = [
         'float32', 'float64']
        for dtype in dtypes:
            x = jt.random([1, 2, 3], dtype)
            res = x.data
            if res.dtype == dtype:
                raise res.shape == (1, 2, 3) or AssertionError

    def test_set_seed(self):
        a = jt.random([1, 2, 3]).data
        b = jt.random([1, 2, 3]).data
        assert str(a) != str(b)
        jt.set_seed(1)
        a = jt.random([1, 2, 3]).data
        jt.set_seed(1)
        b = jt.random([1, 2, 3]).data
        assert str(a) == str(b)

    def test_array_op(self):
        data = [
         np.array([1, 2, 3]),
         np.int32([1, 2, 3]),
         np.int64([1, 2, 3]),
         np.float32([1, 2, 3]),
         np.float64([1, 2, 3])]
        for a in data:
            assert sum(jt.array(a).data) == 6

        assert np.all(jt.array(np.int32([1, 2, 3])[::-1]).data == [3, 2, 1])
        assert jt.array(1).data.shape == (1, )

    def test_matmul_op(self):
        a = np.array([[1, 0], [0, 1]]).astype('float32')
        b = np.array([[4, 1], [2, 2]]).astype('float32')
        c = np.matmul(a, b)
        jtc = jt.matmul(jt.array(a), jt.array(b)).data
        assert np.all(jtc == c)

    def test_var_holder(self):
        jt.clean()
        expect_error(lambda : jt.matmul(1, 1))
        expect_error(lambda : jt.matmul([1], [1]))
        expect_error(lambda : jt.matmul([[1]], [1]))
        self.assertEqual(jt.number_of_lived_vars(), 0)
        a = jt.matmul(jt.float32([[3]]), jt.float32([[4]])).data
        if not (a.shape == (1, 1) and a[(0, 0)] == 12):
            raise AssertionError
        a = np.array([[1, 0], [0, 1]]).astype('float32')
        b = np.array([[4, 1], [2, 2]]).astype('float32')
        c = np.matmul(a, b)
        jtc = jt.matmul(jt.array(a), jt.array(b)).data
        assert np.all(jtc == c)


if __name__ == '__main__':
    unittest.main()