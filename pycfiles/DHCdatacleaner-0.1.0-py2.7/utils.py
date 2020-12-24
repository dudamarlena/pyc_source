# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/DHCdatacleaner/utils.py
# Compiled at: 2018-04-23 22:03:40
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
from sklearn.model_selection import StratifiedKFold
import argparse
from update_checker import update_check
update_checked = False

def auto_sel_cols(input_dataframe):
    """
    Parameter
        -----
        :param input_dataframe:pd.DataFrame 
    
    Return
        ------
        :con_cols:list of col names identified as continuous cols
        :cat_cols:list of col names identified as categorical cols
    """
    con_cols = []
    cat_cols = []
    for column in input_dataframe.columns.values:
        column_type = None
        try:
            map(float, input_dataframe[column].unique())
            column_type = 1
        except:
            column_type = 2

        if column_type == 1:
            con_cols.append(column)
        elif column_type == 2:
            cat_cols.append(column)

    print('continuous:', pd.Series(con_cols))
    print('categorical:', pd.Series(cat_cols))
    return (con_cols, cat_cols)


def replace_value(input_dataframe, sel_cols, val_list, val_rep, copy=False):
    """
    Parameter
        -----
        :param input_dataframe: pandas.DataFrame
        :param sel_cols: list, selected columns need to replace,
        :param val_list: list,values needs to be replaced,
        :param val_rep:  list,values used to replace,
        :param copy:  copy the data or not,
    Return
        -----
        :input_dataframe:dataframe with value replaced
    """
    if copy:
        input_dataframe = input_dataframe.copy()
    input_dataframe[sel_cols].replace(val_list, val_rep, inplace=True)
    return input_dataframe