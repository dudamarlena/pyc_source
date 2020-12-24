# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tests/bpr_test.py
# Compiled at: 2019-10-24 04:10:23
# Size of source mod 2**32: 1102 bytes
import unittest
from scipy.sparse import csr_matrix
from implicit.bpr import BayesianPersonalizedRanking
from implicit.cuda import HAS_CUDA
from .recommender_base_test import TestRecommenderBaseMixin

class BPRTest(unittest.TestCase, TestRecommenderBaseMixin):

    def _get_model(self):
        return BayesianPersonalizedRanking(factors=3, regularization=0, use_gpu=False)

    def test_fit_empty_matrix(self):
        raw = [
         [
          0, 0, 0], [0, 0, 0], [0, 0, 0]]
        return BayesianPersonalizedRanking().fit((csr_matrix(raw)), show_progress=False)

    def test_fit_almost_empty_matrix(self):
        raw = [
         [
          0, 0, 0], [0, 1, 0], [0, 0, 0]]
        return BayesianPersonalizedRanking().fit((csr_matrix(raw)), show_progress=False)


if HAS_CUDA:

    class BPRGPUTest(unittest.TestCase, TestRecommenderBaseMixin):

        def _get_model(self):
            return BayesianPersonalizedRanking(factors=3, regularization=0, use_gpu=True)


if __name__ == '__main__':
    unittest.main()