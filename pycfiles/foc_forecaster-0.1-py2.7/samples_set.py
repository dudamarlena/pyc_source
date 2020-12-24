# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/forecaster/tests/samples_set.py
# Compiled at: 2012-01-10 04:55:24
"""
Created on 16. 12. 2011.

@author: kermit
"""
import unittest
from forecaster.ai.samples_set import SamplesSet

class Test(unittest.TestCase):

    def test_build(self):
        look_back_years = 3
        samples_set = SamplesSet(look_back_years)
        samples_set.t_loc = 'test_sample_selection.xls'
        train_samples, test_samples = samples_set.build_from_crises_file(['usa', 'deu'], ['SP.POP.65UP.TO.ZS'], 0.5)
        self.assertEqual(len(train_samples), 4)
        self.assertEqual(len(test_samples), 3)


if __name__ == '__main__':
    unittest.main()