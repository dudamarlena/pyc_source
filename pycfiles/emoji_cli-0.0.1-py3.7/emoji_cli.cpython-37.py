# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\emoji_cli\emoji_cli.py
# Compiled at: 2019-04-12 00:50:10
# Size of source mod 2**32: 947 bytes
"""
Desc: Opencc python module.
Author: binbin.hou
Date: 2019-4-10 13:40:20
Since: 0.0.1
"""
import fire
from emoji_cli.emoji_dict import dict_singleton

class EmojiCli(object):
    __doc__ = '\n    1. 当前版本暂时不支持分词\n    2. 准备下一期添加分词功能\n    '

    @staticmethod
    def emoji(name):
        """
        获取 emoji 说明的结果
        1. name 目前支持英文，大小写不限
        :param name: 目前支持英文，大小写不限
        :return: 对应的 emoji 列表信息
        """
        print(' '.join(dict_singleton.emoji(name)))

    @staticmethod
    def name(emoji):
        """
        获取 emoji 对应的英文
        :param emoji: emoji 表情
        :return: 对应的名称
        """
        print(dict_singleton.name(emoji))


def main():
    fire.Fire(EmojiCli)


if __name__ == '__main__':
    main()