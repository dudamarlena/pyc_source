# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/DHCdatacleaner/categorical.py
# Compiled at: 2018-05-01 23:52:13
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
import pandas as pd
from utils import replace_value
from sklearn.preprocessing import LabelEncoder
import argparse
from update_checker import update_check
update_checked = False

def missing_value_clean(input_dataframe, sel_cols, drop_nans=False, method='mode', copy=False):
    """Performs a series of automated data cleaning transformations on the provided data set

    Parameters
        ----------
        input_dataframe: pandas.DataFrame
            Data set to clean
        sel_cols:
            Categorical columns selected
        drop_nans: bool
            Drop all rows that have a NaN in any column (default: False)
        method:string
            Method used, can be {'mode','bffill'}
        copy: bool
            Make a copy of the data set (default: False)
    Returns
        ----------
        output_dataframe: pandas.DataFrame
            Cleaned data set

    """
    assert method in {'mode', 'bffill'}
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
        print(column, 'missing percentage:', float(len(input_dataframe[(input_dataframe[column].isnull() == True)])) / len(input_dataframe[column]))
        if method == 'mode':
            most_frequent = input_dataframe[column].mode()
            if len(most_frequent) > 0:
                print('mode fill is used')
                input_dataframe[column].fillna(input_dataframe[column].mode()[0], inplace=True)
        elif method == 'bffill':
            print('bfill and ffill is used')
            input_dataframe[column].fillna(method='bfill', inplace=True)
            input_dataframe[column].fillna(method='ffill', inplace=True)

    print('Done!')
    return input_dataframe


def word_num_encode(input_dataframe, sel_cols, copy=False, encoder=None, encoder_kwargs=None):
    """Performs a series of automated data cleaning transformations on the provided data set

    Parameters
        ----------
        input_dataframe: pandas.DataFrame
            Data set to clean
        sel_cols: list
            Categorical columns selected
        copy: bool
            Make a copy of the data set (default: False)
        encoder: category_encoders transformer
            The a valid category_encoders transformer which is passed an inferred cols list. Default (None: LabelEncoder)
        encoder_kwargs: category_encoders
            The a valid sklearn transformer to encode categorical features. Default (None)
    
    Returns
        ----------
        output_dataframe: pandas.DataFrame
            Cleaned data set

    """
    if copy:
        input_dataframe = input_dataframe.copy()
    if encoder_kwargs is None:
        encoder_kwargs = {}
    print('columns to clean:')
    for column in sel_cols:
        print(column)
        if str(input_dataframe[column].values.dtype) == 'object':
            if encoder is not None:
                print('encoder set by the user is used')
                column_encoder = encoder(**encoder_kwargs).fit(input_dataframe[column].values)
            else:
                print('default encoding method is used')
                column_encoder = LabelEncoder().fit(input_dataframe[column].values)
            input_dataframe[column] = column_encoder.transform(input_dataframe[column].values)

    print('Done!')
    return input_dataframe