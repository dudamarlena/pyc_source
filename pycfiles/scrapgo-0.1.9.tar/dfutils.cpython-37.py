# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\lib\dataframe\dfutils.py
# Compiled at: 2019-05-29 13:59:12
# Size of source mod 2**32: 887 bytes
import pandas as pd

def _get_index_mask(dataframe, other, index, how):
    df_index = dataframe[index].set_index(index).index
    oth_index = other[index].set_index(index).index
    mask = df_index.isin(oth_index)
    if how == 'diff':
        return ~mask
    return mask


def _filter_by_index_mask(dataframe, index, mask):
    dataframe = dataframe.set_index(index)
    filterd = dataframe.loc[mask]
    dataframe = filterd.reset_index()
    return dataframe


def get_intersect_with(dataframe, other, index):
    mask = _get_index_mask(dataframe, other, index, 'intersect')
    dataframe = _filter_by_index_mask(dataframe, index, mask)
    return dataframe


def get_difference_from(dataframe, other, index):
    mask = _get_index_mask(dataframe, other, index, 'diff')
    dataframe = _filter_by_index_mask(dataframe, index, mask)
    return dataframe