# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_rplot.py
# Compiled at: 2017-06-02 17:59:41
import unittest, numpy as np, matplotlib as mpl
mpl.use('Agg')
import scipyplot as spp

class TestRplot(unittest.TestCase):

    def test_rplot_vector(self):
        y = np.random.rand(100)
        h = spp.rplot(y=y)

    def test_rplot_matrix1d(self):
        y = np.random.rand(100, 1)
        h = spp.rplot(y=y)

    def test_rplot_list1d(self):
        y = [
         np.random.rand(100), np.random.rand(100)]
        h = spp.rplot(y=y)

    def test_rplot_list(self):
        y = [
         np.random.rand(100, 1), np.random.rand(100, 1)]
        h = spp.rplot(y=y)

    def test_rplot_matrix(self):
        y = np.random.rand(100, 5)
        h = spp.rplot(y=y)

    def test_rplot_vector_x(self):
        y = np.random.rand(100)
        x = np.random.rand(100)
        h = spp.rplot(y=y, x=x)

    def test_rplot_matrix1d_x(self):
        y = np.random.rand(100, 1)
        x = np.random.rand(100, 1)
        h = spp.rplot(y=y, x=x)

    def test_rplot_list1d(self):
        y = [
         np.random.rand(100), np.random.rand(100)]
        h = spp.rplot(y=y)

    def test_rplot_list(self):
        y = [
         np.random.rand(100, 1), np.random.rand(100, 1)]
        h = spp.rplot(y=y)

    def test_rplot_matrix_x(self):
        y = np.random.rand(100, 5)
        x = np.random.rand(100)
        h = spp.rplot(y=y, x=x)


if __name__ == '__main__':
    unittest.main()