# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\emoji_cli\emoji_util.py
# Compiled at: 2019-04-12 01:40:44
# Size of source mod 2**32: 860 bytes
"""
Desc: Emoji python util module.
Author: binbin.hou
Date: 2019-4-11 20:23:51
Since: 0.0.1
"""

class StrUtil(object):
    EMPTY = ''
    BLANK = ' '
    COMMA = ','

    @staticmethod
    def is_empty(target):
        """
        是否为空
        1. 如果为 None 或者为 ""，则返回真
        2. 其他为假
        :param target:入参
        :return:是否为空
        """
        if not target:
            return True
        if target == StrUtil.EMPTY:
            return True
        return False

    @staticmethod
    def is_not_empty(target):
        """
        是否不为空，和 is_empty 相反
        :param target:入参
        :return:是否不为空
        """
        return not StrUtil.is_empty(target)