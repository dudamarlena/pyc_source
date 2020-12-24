# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/DHCdatacleaner/transform.py
# Compiled at: 2018-04-25 04:28:16
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
import pandas as pd, numpy as np, re
from sklearn.preprocessing import LabelEncoder
import argparse
from update_checker import update_check
update_checked = False

def function_derive(input_dataframe, sel_cols, new_cols, function, copy=False):
    """
    Parameter
        -----
        :param input_dataframe: pd.Dataframe
        :param sel_col: should be a list
            input column name
        :param new_col: should be a list
            ouput column name
        :param function: sould be a function
            ex.def change(x):
                if x>20 and x<=30:
                    y=1
                elif x>30:
                    y=2
                else:
                    y=0
                return y
        :param append: bool
            if True append the derived col to the original dataset, default True
        :param copy: bool
            if True make a copy of the dataframe
    Return
    -----
        :input_dataframe:dataframe with new features
    """
    if copy:
        input_dataframe = input_dataframe.copy()
    assert function.func_name
    assert type(input_dataframe) == pd.DataFrame
    assert type(sel_cols) == list and type(new_cols) == list
    assert len(sel_cols) == len(new_cols)

    def derive(sel_col, new_col):
        input_dataframe[new_col] = map(function, input_dataframe[sel_col])

    map(derive, sel_cols, new_cols)
    return input_dataframe


def one_hot_derive(input_dataframe, sel_col, seperator=None, copy=False):
    """
    One Hot transform for categorical col,only one col is supported.
    Parameters
        -----
        :param input_dataframe: pd.DataFrame
        :param sel_col: list,
            must be one col as this is one-hot transfer
        :param seperator: should be a string or None or whatever separates the features in the content of the data.
            The seperator Used in the values,
            ex.
            if you use',' as seperator,
         'A,B,C' will be detected as 3 values ['A','B','C']
        :param copy:bool
         whether copy the dataset or not
    Return
    -----
    :input_dataframe:dataframe with new features
    :vals:a list of values detected,names of the derived cols
    """
    assert len(sel_col) == 1
    if copy:
        input_dataframe = input_dataframe.copy()

    def to_list(x):
        if type(x) == int or type(x) == float:
            x = str(x)
        try:
            l1 = x.split(seperator)

            def f(x):
                return len(x) > 0

            l2 = list(filter(f, set(l1)))
            l2 = list(set(l2))
            return l2
        except:
            return []

    ls = map(to_list, input_dataframe[sel_col[0]])
    ls = list(np.unique(ls))

    def add(x, y):
        return list(set(x + y))

    vals = reduce(add, ls)
    vals = list(set(vals))

    def one_hot(x, y):
        if type(x) == int or type(x) == float:
            x = str(x)
        try:
            return y in x
        except:
            return 1 == 2

    def derive_one_hot(val):
        try:
            assert val not in input_dataframe.columns
        except AssertionError:
            print('Warning:', val, 'is in the features already,you are trying to replace it.')

        iter = [
         val] * len(input_dataframe)
        result = pd.Series(map(one_hot, input_dataframe[sel_col[0]], iter), index=input_dataframe.index)
        input_dataframe[val] = result

    map(derive_one_hot, vals)
    return (input_dataframe, vals)


def re_extraction(input_dataframe, sel_cols, new_cols, re_method, copy=False):
    """
    Parameter
        -----
        :param input_dataframe: pd.DataFrame
        :param sel_cols: list,cols to extract from
        :param new_cols: list,new cols
        :param re_method: regularization expression
        :param copy: bool,whether to copy or not
    Return
        -----
        : input_dataframe
    """
    if copy == True:
        input_dataframe = input_dataframe.copy()
    assert type(sel_cols) == list and type(new_cols) == list
    assert len(sel_cols) == len(new_cols)
    for i in range(len(sel_cols)):
        col = sel_cols[i]
        new_col = new_cols[i]
        index = input_dataframe[col].isnull().values == False
        try:
            val_re = input_dataframe[col][index].map(lambda x: re.findall(re_method, x))
            input_dataframe[new_col] = val_re
        except:
            print('Columns Extraction Warning:', col)

    return input_dataframe