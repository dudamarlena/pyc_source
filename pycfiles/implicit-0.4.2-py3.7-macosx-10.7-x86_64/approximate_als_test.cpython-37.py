# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tests/approximate_als_test.py
# Compiled at: 2019-10-24 03:58:04
# Size of source mod 2**32: 3372 bytes
from __future__ import print_function
import unittest
from implicit.approximate_als import AnnoyAlternatingLeastSquares, FaissAlternatingLeastSquares, NMSLibAlternatingLeastSquares
from implicit.cuda import HAS_CUDA
from .recommender_base_test import TestRecommenderBaseMixin
try:
    import annoy

    class AnnoyALSTest(unittest.TestCase, TestRecommenderBaseMixin):

        def _get_model(self):
            return AnnoyAlternatingLeastSquares(factors=2, regularization=0, use_gpu=False)

        def test_pickle(self):
            pass


except ImportError:
    pass

try:
    import nmslib

    class NMSLibALSTest(unittest.TestCase, TestRecommenderBaseMixin):

        def _get_model(self):
            return NMSLibAlternatingLeastSquares(factors=2, regularization=0, index_params={'post': 2},
              use_gpu=False)

        def test_pickle(self):
            pass


except ImportError:
    pass

try:
    import faiss

    class FaissALSTest(unittest.TestCase, TestRecommenderBaseMixin):

        def _get_model(self):
            return FaissAlternatingLeastSquares(nlist=1, nprobe=1, factors=2, regularization=0, use_gpu=False)

        def test_pickle(self):
            pass


    if HAS_CUDA:

        class FaissALSGPUTest(unittest.TestCase, TestRecommenderBaseMixin):
            _FaissALSGPUTest__regularization = 0

            def _get_model(self):
                return FaissAlternatingLeastSquares(nlist=1, nprobe=1, factors=32, regularization=(self._FaissALSGPUTest__regularization),
                  use_gpu=True)

            def test_similar_items(self):
                self._FaissALSGPUTest__regularization = 1.0
                try:
                    super(FaissALSGPUTest, self).test_similar_items()
                finally:
                    self._FaissALSGPUTest__regularization = 0.0

            def test_large_recommend(self):
                plays = self.get_checker_board(2048)
                model = self._get_model()
                model.fit(plays, show_progress=False)
                recs = model.similar_items(0, N=1050)
                self.assertEqual(recs[0][0], 0)
                recs = model.recommend(0, (plays.T.tocsr()), N=1050)
                self.assertEqual(recs[0][0], 0)

            def test_pickle(self):
                pass


except ImportError:
    pass

if __name__ == '__main__':
    unittest.main()