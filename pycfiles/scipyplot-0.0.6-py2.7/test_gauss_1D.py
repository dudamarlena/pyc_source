# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_gauss_1D.py
# Compiled at: 2017-06-02 18:05:51
import unittest, numpy as np, matplotlib as mpl
mpl.use('Agg')
import scipyplot as spp

class TestRplot(unittest.TestCase):

    def test_gauss_1D_vector(self):
        y = np.random.rand(100)
        variance = np.random.rand(100)
        h = spp.gauss_1D(y=y, variance=variance)


if __name__ == '__main__':
    unittest.main()