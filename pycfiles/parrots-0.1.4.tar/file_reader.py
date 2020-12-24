# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xuming06/Codes/parrots/parrots/utils/file_reader.py
# Compiled at: 2018-08-26 22:54:43
"""
@author:XuMing（xuming624@qq.com)
@description: 获取符号字典列表的程序
"""

def get_pinyin_list(dict_path=''):
    u"""
    加载拼音符号列表，用于标记符号
    :param dict_path: 拼音符号列表
    :return:
    """
    list_symbol = []
    pinyin_idx = 0
    with open(dict_path, mode='r', encoding='UTF-8') as (f):
        for line in f:
            line = line.strip('\n')
            parts = line.split('\t')
            list_symbol.append(parts[pinyin_idx])

    list_symbol.append('_')
    return list_symbol