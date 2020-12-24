# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/data/binary_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 960 bytes
"""
@author = super_fazai
@File    : binary_utils.py
@connect : superonesfazai@gmail.com
"""
from binascii import a2b_hex, b2a_hex
__all__ = [
 'int_to_8_digit_sixteen_digit_num',
 'hex_2_str',
 'str_2_hex']

def int_to_8_digit_sixteen_digit_num(i: int) -> str:
    """
    整数转换为8位十六进制数
    :param i:
    :return:
    """
    hexrep = format(i, '08x')
    thing = ''
    for i in (3, 2, 1, 0):
        thing += hexrep[2 * i:2 * i + 2]

    return thing


def hex_2_str(target) -> bytes:
    """
    16进制转文本
    :param target: 16进制字符串
    :return:
    """
    return a2b_hex(target)


def str_2_hex(target) -> bytes:
    """
    文本转16进制
    :param target:
    :return:
    """
    return b2a_hex(target)