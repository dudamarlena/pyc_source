# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/philippos/Desktop/Dev_OpenSource/transitionMatrix/tests/test_datasets.py
# Compiled at: 2018-10-16 05:05:48
# Size of source mod 2**32: 1338 bytes
import unittest, transitionMatrix as tm
from datasets import Minimal
from transitionMatrix import dataset_path
ACCURATE_DIGITS = 7

class TestDatasets(unittest.TestCase):
    __doc__ = '\n    Load in-memory matrices\n    '

    def test_minimal_matrix(self):
        a = tm.TransitionMatrix(values=Minimal)
        a.validate()
        self.assertEqual(a.dimension, 3)

    def test_matrix_set_load_csv(self):
        a = tm.TransitionMatrixSet(csv_file=dataset_path + 'sp_1981-2016.csv', temporal_type='Cumulative')
        a.validate()
        self.assertEqual(a.periods, [1, 2, 3, 5, 7, 10, 15, 20])


if __name__ == '__main__':
    unittest.main()