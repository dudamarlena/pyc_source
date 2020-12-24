# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pre_json/pd_json.py
# Compiled at: 2019-06-25 04:51:43
# Size of source mod 2**32: 582 bytes
"""
@author: magician
@file: pd_json.py
@date: 2019/06/05
"""
import pandas as pd

def read_json(file, **kwargs):
    """
    read json
    :param file:    json
    :param kwargs:
    :return: DataFrame
    """
    json_df = pd.read_json(file, **kwargs)
    return json_df


def write_json(df, **kwargs):
    """
    write json
    :param df:
    :param kwargs: orient
    :return: json
    """
    orient = kwargs.get('orient', 'index')
    json_df = df.to_json(orient=orient, force_ascii=False, **kwargs)
    return json_df