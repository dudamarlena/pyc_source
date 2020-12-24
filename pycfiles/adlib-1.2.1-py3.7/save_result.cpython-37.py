# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/utils/save_result.py
# Compiled at: 2018-07-20 16:00:09
# Size of source mod 2**32: 374 bytes
import pandas as pd

def save_result(result_arr, column_name):
    """
    result -> pandas Dataframe structure
    :param result_arr: np.array type
    :param column_name: list
    :return: csv file
    """
    df = pd.DataFrame(result_arr, column_name)