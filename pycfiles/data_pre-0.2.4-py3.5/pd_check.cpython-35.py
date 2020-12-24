# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pre/pd_check.py
# Compiled at: 2019-06-25 04:51:43
# Size of source mod 2**32: 988 bytes
"""
@author: magician
@file: excel.py
@date: 2018/12/17
"""
import pandas as pd

def check_data_type(col_name, value, check_type, **kwargs):
    """
    字符串检查
    :param col_name:       列名
    :param value:          检查元素
    :param check_type:     检查类型
    :param kwargs:
    """
    result = ''
    if value or value == 0:
        if check_type == 'datetime':
            try:
                pd.to_datetime(value)
            except Exception as e:
                print(e)
                result = col_name + '时间类型错误' + ': ' + str(value) + ' '

        elif not isinstance(value, check_type):
            result = col_name + '类型错误' + ': ' + str(value) + ' '
    else:
        result = col_name + '不能为空'
    return result