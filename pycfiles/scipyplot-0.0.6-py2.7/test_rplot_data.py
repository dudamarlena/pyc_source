# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_rplot_data.py
# Compiled at: 2017-06-02 17:59:41
import unittest, numpy as np, matplotlib as mpl
mpl.use('Agg')
import scipyplot as spp, matplotlib.pyplot as plt

class TestRplot(unittest.TestCase):

    def test_rplot_data_1(self):
        y = [
         np.random.rand(100, 100)]
        h = spp.rplot_data(data=y)

    def test_rplot_data_2(self):
        y = [
         np.random.rand(100, 100)]
        x = [np.random.rand(100)]
        h = spp.rplot_data(data=y)

    def test_rplot_data_3(self):
        y = [
         np.random.rand(100, 100)]
        x = np.random.rand(100)
        h = spp.rplot_data(data=y)

    def test_rplot_data_yscale(self):
        y = [
         np.absolute(np.random.rand(100, 100)) + 1e-05]
        x = np.random.rand(100)
        h = spp.rplot_data(data=y)
        plt.yscale('log')

    def test_rplot_data_matrix(self):
        y = np.random.rand(100, 100)
        h = spp.rplot_data(data=y)


if __name__ == '__main__':
    unittest.main()