# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\test\test_emoji_dict.py
# Compiled at: 2019-04-11 22:48:27
# Size of source mod 2**32: 516 bytes
from emoji_cli.emoji_dict import *

class TestEmojiDict(object):

    def test_name(self):
        """
        测试名称
        :return: none
        """
        emoji_dict = Dict()
        assert 'redheart' == emoji_dict.name('❤')

    def test_emoji(self):
        """
        测试表情
        :return: none
        """
        emoji_dict = Dict()
        assert ['❤'] == emoji_dict.emoji('redheart')