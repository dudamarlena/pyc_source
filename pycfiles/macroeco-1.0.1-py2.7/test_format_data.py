# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/macroeco/misc/test_format_data.py
# Compiled at: 2015-09-02 15:37:13
from __future__ import division
from numpy.testing import TestCase, assert_equal, assert_array_equal, assert_almost_equal, assert_array_almost_equal, assert_allclose, assert_, assert_raises
import numpy as np
from macroeco.misc import *
import pandas as pd

class TestFormatData(TestCase):

    def test_simple_stack(self):
        test_data = pd.DataFrame({'row': [1, 2, 1, 2], 'column': [
                    1, 1, 2, 2], 
           'labelA': [1, 0, 3, 4], 'labelB': [
                    3, 2, 1, 4]})
        expected = pd.DataFrame({'row': [1, 1, 2, 2, 1, 1, 2, 2], 'column': [
                    1, 1, 1, 1, 2, 2, 2, 2], 
           'label': np.tile(['labelA', 'labelB'], 4), 'count': [
                   1, 3, 0, 2, 3, 1, 4, 4]}, columns=['row', 'column', 'label',
         'count'])
        stack = format_dense(test_data, ['row', 'column'])
        assert_equal(np.all(stack == expected), True)

    def test_label_count_col(self):
        test_data = pd.DataFrame({'year': ['02', '03'], 'spp1': [1, 2], 'spp2': [
                  3, 4]})
        expected = pd.DataFrame({'year': np.repeat(['02', '03'], 2), 'spp': np.tile(['spp1', 'spp2'], 2), 
           'ind': [1, 3, 2, 4]}, columns=['year',
         'spp', 'ind'])
        stack = format_dense(test_data, ['year'], label_col='spp', count_col='ind')
        print stack
        print expected
        assert_equal(np.all(stack == expected), True)

    def test_drop_nan(self):
        test_data = pd.DataFrame({'year': ['02', '03'], 'spp1': [1, np.nan], 'spp2': [
                  np.nan, 4]})
        expected = pd.DataFrame({'year': ['02', '03'], 'label': [
                   'spp1', 'spp2'], 
           'count': [1, 4]}, columns=['year',
         'label', 'count'])
        stack = format_dense(test_data, ['year'], drop_na=True)
        assert_equal(np.all(stack == expected), True)

    def test_nan_to_zero(self):
        test_data = pd.DataFrame({'year': ['02', '03'], 'spp1': [1, np.nan], 'spp2': [
                  np.nan, 4]})
        expected = pd.DataFrame({'year': np.repeat(['02', '03'], 2), 'label': np.tile(['spp1', 'spp2'], 2), 
           'count': [1, 0, 0, 4]}, columns=['year',
         'label', 'count'])
        stack = format_dense(test_data, ['year'], nan_to_zero=True)
        assert_equal(np.all(stack == expected), True)