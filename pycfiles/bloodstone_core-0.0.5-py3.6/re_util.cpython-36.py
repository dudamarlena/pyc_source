# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmpy_util/re_util.py
# Compiled at: 2019-12-17 02:28:10
# Size of source mod 2**32: 2494 bytes
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : re_util.py
@Desc    : 通过正则表达式处理字符串工具模块
"""
import re, traceback

def hump2underline(hump_str):
    """
    驼峰形式字符串转成下划线形式
    :param hump_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    """
    p = re.compile('([a-z]|\\d)([A-Z])')
    sub = re.sub(p, '\\1_\\2', hump_str).lower()
    return sub


def underline2hump(underline_str):
    """
    下划线形式字符串转成驼峰形式
    :param underline_str: 下划线形式字符串
    :return: 驼峰形式字符串
    """
    sub = re.sub('(_\\w)', lambda x: x.group(1)[1].upper(), underline_str)
    return sub


array_word_pattern = re.compile('^(?P<key>\\w*)(?P<bracket>\\[(?P<index>\\d*)\\])?$')

def process_array_word(array_word):
    """
    处理数组格式的文字.eg num[0]，返回实际key和对应的index .eg ('num', 0)
    :return:
    """
    try:
        match = array_word_pattern.match(array_word)
        if match is not None:
            key = match.group('key')
            bracket = match.group('bracket')
            index = match.group('index')
            index_num = None
            if bracket is not None:
                if index == '':
                    index_num = 0
                else:
                    index_num = int(index)
            return (
             key, index_num)
    except Exception as error:
        print(traceback.print_exc())

    return (None, None)


def remove_num(text):
    """
    移除文字当中的数字
    :param text:
    :return:
    """
    p = re.compile('\\d')
    return re.sub(p, '', text)


def trans(x):
    print(x)
    g = x.group(0)
    g1 = g[1]
    return x.group(1)[1].upper()


if __name__ == '__main__':
    result = process_array_word('num[0]')
    result = process_array_word('fail_num')
    print(result)