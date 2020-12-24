# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/data/str_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 1737 bytes
"""
@author = super_fazai
@File    : str_utils.py
@Time    : 2016/8/4 13:15
@connect : superonesfazai@gmail.com
"""
__all__ = [
 'char_is_alphabet',
 'char_is_chinese',
 'char_is_number',
 'char_is_other',
 'str_2_unicode']

def char_is_alphabet(uchar):
    """
    判断单个字符是否是英文字母
    :param uchar: 单个字符
    :return: bool
    """
    if not 'A' <= str(uchar) <= 'Z':
        if 'a' <= str(uchar) <= 'z':
            return True
    return False


def char_is_chinese(uchar):
    """
    判断单个字符是否是汉字
    :param uchar: 单个字符
    :return: bool
    """
    if '一' <= str(uchar) <= '龥':
        return True
    return False


def char_is_number(uchar):
    """
    判断单个字符是否是数字
    :param uchar: 单个字符
    :return: bool
    """
    if '0' <= str(uchar) <= '9':
        return True
    return False


def char_is_other(uchar):
    """
    判断单个字符是否非汉字，数字和英文字符
    :param uchar:
    :return:
    """
    uchar = str(uchar)
    if not char_is_chinese(uchar):
        if not char_is_number(uchar):
            if not char_is_alphabet(uchar):
                return True
    return False


def str_2_unicode(target: str):
    """
    str 转 unicode
    :param target:
    :return:
    """
    return target.encode('unicode_escape').decode('utf-8')