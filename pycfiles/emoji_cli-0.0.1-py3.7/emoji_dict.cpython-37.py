# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\emoji_cli\emoji_dict.py
# Compiled at: 2019-04-12 01:39:25
# Size of source mod 2**32: 2365 bytes
"""
Desc: Emoji python dict module.
Author: binbin.hou
Date: 2019-4-11 20:24:25
Since: 0.0.1
"""
import os
from io import open
from emoji_cli import emoji_const as const
from emoji_cli.emoji_util import *

class Dict(object):
    __doc__ = '\n    获取字典信息\n    '
    _Dict__emoji_info_dict = {}
    _Dict__current_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        """
        内部初始化
        """
        self._Dict__init_dict(const.EMOJI_DATA_PATH, self._Dict__emoji_info_dict)

    def __init_dict(self, relative_path, emoji_dict):
        """
        初始化所有的字典信息
        1. 跳过空白行
        2. 跳过#开头的行（实际为分组）
        :param relative_path: 相对文件路径
        :param emoji_dict: 原始集合
        :return: 无
        """
        with open((self._Dict__current_path + relative_path), mode='r', encoding=(const.DEFAULT_CHARSET)) as (stc):
            for line in stc:
                if line.startswith('#'):
                    continue
                if StrUtil.is_empty(line.strip()):
                    continue
                lines = line.split(StrUtil.COMMA)
                emoji_dict[lines[0]] = lines[1].strip()

    def name(self, emoji):
        """
        获取 emoji 对应的英文名称
        :param emoji: emoji 字符
        :return: 英文名称
        """
        return self._Dict__get_val(emoji, self._Dict__emoji_info_dict)

    def emoji(self, english_name):
        """
        获取 emoji 对应的英文名称
        :param english_name: 英文名称
        :return: 表情列表
        """
        result_list = []
        for key, value in self._Dict__emoji_info_dict.items():
            if value.find(english_name) >= 0:
                result_list.append(key)

        return result_list

    @staticmethod
    def __get_val(key, _Dict__dict):
        """
        获取对应的值
        1. 如果 key 为空，直接返回
        2. 如果没获取到值，默认返回 key
        :param key: 入参
        :param __dict: 对应的字典信息
        :return: 结果
        """
        result = _Dict__dict.get(key, StrUtil.EMPTY)
        return result


dict_singleton = Dict()