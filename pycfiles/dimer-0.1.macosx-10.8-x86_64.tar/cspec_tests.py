# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/nnet/cspec_tests.py
# Compiled at: 2013-07-10 19:56:04
import unittest, numpy as np
rng = np.random.RandomState()
from config_spec import DataSpec

class Test(unittest.TestCase):

    def testDataSpec(self):
        for i in range(5):
            a, b = DataSpec.batches_from_data(rng.randint(100, 1000), 5, rng.randint(1, 10) / 20.0, i, rng)
            self.assertEqual(list(set(a + b)), range(len(a + b)))
            self.assertTrue(i in b)


if __name__ == '__main__':
    unittest.main()