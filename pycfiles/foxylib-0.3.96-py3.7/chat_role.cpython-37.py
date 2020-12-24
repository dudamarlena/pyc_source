# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/khalalib/chat/chat_role.py
# Compiled at: 2019-12-17 01:13:16
# Size of source mod 2**32: 1478 bytes
import re
from future.utils import lfilter
from nose.tools import assert_is_not_none
from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.regex.regex_tool import MatchTool
from foxylib.tools.string.string_tool import str2strip
from khalalib.chat.chat import KhalaChat

class ChatRole:
    COMMAND = 'command'

    class Value:
        COMMAND = 'command'

    V = Value

    @classmethod
    def role_class_list(cls):
        return [CommandChatRole]

    @classmethod
    def j_chat2role(cls, chat):
        l_matched = lfilter(lambda x: x.chat2is_role_matched(chat), cls.role_class_list())
        if not l_matched:
            return
        role_class = l_singleton2obj(l_matched)
        return role_class.NAME


class CommandChatRole:
    PREFIX = '?'
    NAME = ChatRole.V.COMMAND

    @classmethod
    def chat2is_role_matched(cls, chat):
        text = KhalaChat.j_chat2text(chat)
        text_stripped = str2strip(text)
        if not text_stripped:
            return False
        else:
            return text_stripped.startswith(cls.PREFIX) or False
        if len(text_stripped) <= 1:
            return False
        return True

    @classmethod
    def chat2command_list(cls, chat):
        text = KhalaChat.j_chat2text(chat)
        m = re.match('{}\\s*'.format(cls.PREFIX), text)
        assert_is_not_none(m)
        i_end = MatchTool.match2end(m)
        str_commands = text[i_end:].split(maxsplit=1)[0]
        return str_commands.split('.')