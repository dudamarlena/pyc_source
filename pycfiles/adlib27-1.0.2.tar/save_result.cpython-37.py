# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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