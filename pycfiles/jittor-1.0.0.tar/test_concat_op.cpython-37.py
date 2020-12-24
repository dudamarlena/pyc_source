# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_concat_op.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 1088 bytes
import unittest, jittor as jt, numpy as np

class TestConcatOp(unittest.TestCase):

    def test_concat_op(self):

        def check(tmp, dim=0):
            res1 = jt.concat(tmp, dim=dim)
            res2 = jt.contrib.concat(tmp, dim=dim)
            assert (res1 != res2).data.sum() == 0, 'concat fail...'

        check([jt.array([[1], [2]]), jt.array([[2], [2]])])
        check([jt.array(range(24)).reshape((1, 2, 3, 4)), jt.array(range(24)).reshape((1, 2, 3, 4))])
        check([jt.array(range(120)).reshape((5, 2, 3, 4)), jt.array(range(24)).reshape((1, 2, 3, 4))])
        check([jt.array(range(5)).reshape((5, 1)), jt.array(range(1)).reshape((1, 1))])
        print('concat success...')


if __name__ == '__main__':
    unittest.main()