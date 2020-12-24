# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pre_pickle/pd_pickle.py
# Compiled at: 2019-06-25 04:51:43
# Size of source mod 2**32: 833 bytes
"""
@author: magician
@file: pd_pickle.py
@date: 2019/06/10
"""
import os, pandas as pd

def read_pickle(file, **kwargs):
    """
    read pickle
    :return:
    """
    pickle_df = pd.read_pickle(file, **kwargs)
    return pickle_df


def write_pickle(df, **kwargs):
    """
    write pickle
    :return:
    """
    file_name = kwargs.get('file_name', '')
    file_path = kwargs.get('file_path', '')
    output_path = os.path.join(file_path, file_name)
    df.to_pickle(output_path, **kwargs)
    return {'file_name': file_name, 
     'output_path': output_path}