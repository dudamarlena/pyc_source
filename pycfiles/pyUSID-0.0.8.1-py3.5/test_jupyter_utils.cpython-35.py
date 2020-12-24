# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/viz/test_jupyter_utils.py
# Compiled at: 2019-11-30 21:58:33
# Size of source mod 2**32: 2212 bytes
"""
Created on Thurs Jun  27 2019

@author: Emily Costa
"""
from __future__ import division, print_function, unicode_literals, absolute_import
import unittest, os, matplotlib as mpl, numpy as np, matplotlib.pyplot as plt
from pyUSID.io.write_utils import Dimension
from pyUSID.viz.jupyter_utils import simple_ndim_visualizer, save_fig_filebox_button
if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

class TestSimpleNdimVisualizer(unittest.TestCase):
    __doc__ = "\n    def test_correct(self):\n        data_mat = np.random.rand(2,3,5,7)\n        x = np.arange(2)\n        y = np.arange(3)\n        z = np.arange(5)\n        w = np.arange(7)\n        pos_dims = [Dimension('X','unit',x), Dimension('Y','unit',y)]\n        spec_dims = [Dimension('Z','unit',z), Dimension('W','unit',w)]\n        simple_ndim_visualizer(data_mat, pos_dims, spec_dims)\n    "

    def test_not_iterable(self):
        arr = np.arange(100).reshape(10, 10)
        num = 1
        with self.assertRaises(TypeError):
            simple_ndim_visualizer(arr, num, num)

    def test_not_dimension_type(self):
        arr = np.arange(100).reshape(10, 10)
        list = [1, 2, 3]
        with self.assertRaises(TypeError):
            simple_ndim_visualizer(arr, list, list)

    def test_too_many_dims(self):
        arr = np.arange(100).reshape(10, 10)
        list = [1, 2, 3]
        with self.assertRaises(TypeError):
            simple_ndim_visualizer(arr, list, list)


class TestSaveFigFileboxButton(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()