# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/DHCdatacleaner/continuous.py
# Compiled at: 2018-05-01 23:53:36
"""
Copyright (c) 2018 Eddie Yi Huang

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from __future__ import print_function
import pandas as pd, numpy as np
from utils import replace_value
from sklearn.preprocessing import LabelEncoder
import argparse

def missing_value_clean(input_dataframe, sel_cols, drop_nans=False, method='median', copy=False):
    """Performs a series of automated data cleaning transformations on the provided data set
    Parameters
        ----------
        input_dataframe: pandas.DataFrame
            Data set to clean
        sel_cols:list
            Continuous columns selected
        drop_nans: bool
            Drop all rows that have a NaN in any column (default: False)
        method:string
            method used to fill missing value,could be in {missing,mean,mode,bffill},default median
        copy: bool
            Make a copy of the data set (default: False)
    Returns
        ----------
        input_dataframe: pandas.DataFrame
            Cleaned data set
    """
    assert method in {'median', 'mean', 'mode', 'bffill'}
    if copy:
        input_dataframe = input_dataframe.copy()
    if drop_nans:
        print('input N:', len(input_dataframe))
        newdata = input_dataframe[sel_cols].dropna()
        index = newdata.index
        input_dataframe = input_dataframe.ix[index, :]
        print('Done!case with any missing value in the selected columns are excluded.Output N:', len(input_dataframe))
        return input_dataframe
    print('columns to clean:')
    for column in sel_cols:
        print(column)
        if method == 'median':
            input_dataframe[column].fillna(input_dataframe[column].median(), inplace=True)
            print('median fill method is used')
        elif method == 'mean':
            input_dataframe[column].fillna(input_dataframe[column].mean(), inplace=True)
            print('mean fill method is used')
        elif method == 'mode':
            most_frequent = input_dataframe[column].mode()
            if len(most_frequent) > 0:
                print('mode fill method is used')
                input_dataframe[column].fillna(input_dataframe[column].mode()[0], inplace=True)
            else:
                print('No mode is Found')
        elif method == 'bffill':
            print('bfill and ffill methods are used')
            input_dataframe[column].fillna(method='bfill', inplace=True)
            input_dataframe[column].fillna(method='ffill', inplace=True)

    print('Done!')
    return input_dataframe


def outlier_detect_clean(input_dataframe, sel_cols, maxv=None, minv=None, method=None, action='replace', copy=False):
    """
    Detect all the outlier numbers and replace them using certain method,or delete them.
    Use Median:
    maxv = median + 1.5 * IQR
    minv=  median - 1.5 * IQR
    Use Mean:
    maxv=mean+2*std
    minv=mean-2*std
    All the Outliers will be replaced by these numbers
    
    Parameters
        ---------
        :param input_dataframe: pd.DataFrame
        Data to clean outliers
        :param sel_cols: columns to use, must be continuous
        :param maxv: max value,can be empty if use 'method'
        :param minv: min value,can be empty if use 'method'
        :param method: None,median or mean
        :param action: to delete or replace the outliers,default replace
        :param copy: whether to copy the data or not 
    Return
        :input_dataframe: pd.DataFrame with outliers cleaned with the specific action.
    """
    if copy:
        input_dataframe = input_dataframe.copy()
    assert method in {None, 'median', 'mean'}
    assert action in {None, 'replace', 'delete'}
    assert type(sel_cols) == list
    for sel_col in sel_cols:
        print(sel_col)
        for u in input_dataframe[sel_col].unique():
            try:
                assert float(u)
            except:
                print(u, 'is not continuous in', sel_col)

        median = input_dataframe[sel_col].median()
        IQR = input_dataframe[sel_col].quantile(0.75) - input_dataframe[sel_col].quantile(0.25)
        mean = input_dataframe[sel_col].mean()
        std = input_dataframe[sel_col].std()
        if method == 'median':
            maxv = median + 1.5 * IQR
            minv = median - 1.5 * IQR
            print('range:', maxv, ',', minv)
        elif method == 'mean':
            maxv = mean + 2 * std
            minv = mean - 2 * std
            print('range:', maxv, ',', minv)
        else:
            assert maxv != None and minv != None
            print('No method is specified,use giving arbitrary range.')
            print('range:', maxv, ',', minv)
        values_counts = input_dataframe[sel_col].value_counts()

        def f(x):
            return x > maxv

        maxout = list(filter(f, values_counts.index))

        def f(x):
            return x < minv

        minout = list(filter(f, values_counts.index))

        def f(x):
            return x > maxv or x < minv

        ls = list(filter(f, values_counts.index))
        outlier = values_counts[ls]
        print('outliers detected:')
        print(list(outlier.index))
        print('Total Outliers:', sum(outlier))
        if action == 'replace':
            print(action, 'action is conducted')
            replace_value(input_dataframe, sel_cols=sel_col, val_list=minout, val_rep=len(minout) * [minv])
            replace_value(input_dataframe, sel_cols=sel_col, val_list=maxout, val_rep=len(maxout) * [maxv])
        elif action == 'delete':
            print(action, 'action is conducted')
            replace_value(input_dataframe, sel_cols=sel_col, val_list=minout, val_rep=len(minout) * [np.nan])
            replace_value(input_dataframe, sel_cols=sel_col, val_list=maxout, val_rep=len(maxout) * [np.nan])
            input_dataframe = input_dataframe.ix[input_dataframe[sel_col].dropna().index, :]
        else:
            print('No action is conducted')

    return input_dataframe