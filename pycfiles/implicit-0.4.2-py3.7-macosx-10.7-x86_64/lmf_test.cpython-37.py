# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tests/lmf_test.py
# Compiled at: 2019-10-24 03:58:04
# Size of source mod 2**32: 355 bytes
import unittest
from implicit.lmf import LogisticMatrixFactorization
from .recommender_base_test import TestRecommenderBaseMixin

class LMFTest(unittest.TestCase, TestRecommenderBaseMixin):

    def _get_model(self):
        return LogisticMatrixFactorization(factors=3, regularization=0, use_gpu=False)


if __name__ == '__main__':
    unittest.main()