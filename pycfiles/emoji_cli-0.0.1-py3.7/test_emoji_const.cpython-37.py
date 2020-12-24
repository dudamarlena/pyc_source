# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\test\test_emoji_const.py
# Compiled at: 2019-04-11 22:35:21
# Size of source mod 2**32: 368 bytes
from emoji_cli import emoji_const as const

class TestEmojiConst(object):

    def test_const(self):
        """
        测试常量
        :return: none
        """
        assert 'UTF-8' == const.DEFAULT_CHARSET
        assert '/db/emoji.data' == const.EMOJI_DATA_PATH