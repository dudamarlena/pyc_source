# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/data/json_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 1172 bytes
"""
@author = super_fazai
@File    : json_utils.py
@Time    : 2016/7/25 09:43
@connect : superonesfazai@gmail.com
"""
import re
from ..common_utils import json_2_dict
__all__ = [
 'read_json_from_local_json_file',
 'nonstandard_json_str_handle']

def read_json_from_local_json_file(json_file_path):
    """
    从本地json文件读取json, 并以dict返回
    :param json_file_path:
    :return: a dict
    """
    try:
        result = ''
        with open(json_file_path, 'r') as (file):
            for item in file.readlines():
                result += item.replace('\n', '')

    except FileNotFoundError as e:
        try:
            print('json path 文件不存在, 请检查!')
            raise e
        finally:
            e = None
            del e

    _ = json_2_dict(json_str=result)
    return _


def nonstandard_json_str_handle(json_str):
    """
    不规范的json_str处理
    :param json_str:
    :return:
    """
    json_str = re.compile('null').sub('""', json_str)
    json_str = re.compile(':,').sub(':"",', json_str)
    return json_str