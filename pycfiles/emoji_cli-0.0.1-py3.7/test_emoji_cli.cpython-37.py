# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\test\test_emoji_cli.py
# Compiled at: 2019-04-11 23:05:41
# Size of source mod 2**32: 790 bytes
from emoji_cli.emoji_cli import *

class TestEmojiCli(object):

    def test_name(self):
        """
        测试名称
        :return: none
        """
        print()
        EmojiCli.name('❤')

    def test_name_not_exists(self):
        """
        测试名称-不存在
        :return: none
        """
        print()
        EmojiCli.name('redheart')

    def test_emoji(self):
        """
        测试表情
        :return: none
        """
        print()
        EmojiCli.emoji('redheart')

    def test_emoji_not_exists(self):
        """
        测试表情-不存在
        :return: none
        """
        print()
        EmojiCli.emoji('❤')