# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_fetcher.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 975 bytes
import unittest, jittor as jt, numpy as np
from jittor import compile_extern

class TestFetcher(unittest.TestCase):

    def test_fetch(self):
        a = jt.array([1, 2, 3])
        a = a * 2
        v = []
        jt.fetch([a], lambda a: v.append(a))
        jt.sync_all(True)
        if not (len(v) == 1 and (v[0] == [2, 4, 6]).all()):
            raise AssertionError


@unittest.skipIf(not jt.has_cuda, 'Cuda not found')
class TestFetcherCuda(TestFetcher):

    @classmethod
    def setUpClass(self):
        jt.flags.use_cuda = 1

    @classmethod
    def tearDownClass(self):
        jt.flags.use_cuda = 0


if __name__ == '__main__':
    unittest.main()