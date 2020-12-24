# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pre/pd_utils.py
# Compiled at: 2019-06-25 04:51:43
# Size of source mod 2**32: 377 bytes
"""
@author: magician
@file: pd_data.py
@date: 2019/06/05
"""

def check_type(data, dtype):
    """
    ckeck data type
    :param data:  data
    :param dtype: data type
    :return: error
    """
    error = ''
    for item in data:
        if not isinstance(item, type(dtype)):
            error = '{0} data type is error!'.format(item)
            break

    return error