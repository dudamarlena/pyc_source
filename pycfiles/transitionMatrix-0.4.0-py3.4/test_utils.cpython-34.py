# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/philippos/Desktop/Dev_OpenSource/transitionMatrix/tests/test_utils.py
# Compiled at: 2018-10-16 05:05:48
# Size of source mod 2**32: 1411 bytes
import unittest, transitionMatrix as tm
from transitionMatrix import source_path
import pandas as pd
ACCURATE_DIGITS = 7

class TestPreprocessing(unittest.TestCase):

    def test_bin_timestamps(self):
        dataset_path = source_path + 'datasets/'
        data = pd.read_csv(dataset_path + 'synthetic_data1.csv')
        event_count = data['ID'].count()
        cohort_data, cohort_intervals = tm.utils.bin_timestamps(data, cohorts=5)
        cohort_data['Count'] = cohort_data['Count'].astype(int)
        self.assertEqual(event_count, cohort_data['Count'].sum())


class TestDataSetGenerators(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()