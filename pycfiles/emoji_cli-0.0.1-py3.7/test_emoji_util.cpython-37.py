# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\test\test_emoji_util.py
# Compiled at: 2019-04-12 01:40:25
# Size of source mod 2**32: 787 bytes
from emoji_cli.emoji_util import *

class TestEmojiUtil(object):
    __doc__ = '\n    测试类\n    '

    def test_is_empty(self):
        """
        测试是否为空
        :return:
        """
        assert True == StrUtil.is_empty(None)
        assert True == StrUtil.is_empty('')
        assert False == StrUtil.is_empty(' ')
        assert False == StrUtil.is_empty('x')

    def test_is_not_empty(self):
        """
        测试是否不为空
        :return:
        """
        assert False == StrUtil.is_not_empty(None)
        assert False == StrUtil.is_not_empty('')
        assert True == StrUtil.is_not_empty(' ')
        assert True == StrUtil.is_not_empty('x')