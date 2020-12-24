# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ProgressedHttp/utils.py
# Compiled at: 2017-10-08 03:38:16
from __future__ import absolute_import, division, print_function
__all__ = [
 'str_len', 'unit_change']

def str_len(s):
    u"""
    获取占用等宽字体终端实际宽度，适用`Monaco`等其他等宽字体字体
    :param s:
    :return:
    """
    length = 0
    for i in s:
        if 3105 <= ord(i) <= 65535:
            length += 2
        else:
            length += 1

    return length


def unit_change(target):
    u"""
    单位换算
    :param target: unsigned int
    :return: str
    """
    if target < 0:
        return str(target)
    unit_list = ('B', 'KB', 'MB', 'GB', 'TB')
    index = 0
    target = float(target)
    while target > 1024:
        index += 1
        target /= 1024

    return ('{:.2f} {}').format(round(target, 2), unit_list[index])