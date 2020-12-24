# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/messenger/slack/events/message.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 452 bytes


class MessageEvent:
    NAME = 'message'

    class Field:
        TYPE = 'type'
        CHANNEL = 'channel'
        USER = 'user'
        TEXT = 'text'
        TS = 'ts'

    F = Field

    @classmethod
    def j2channel_id(cls, j):
        return j[cls.F.CHANNEL]

    @classmethod
    def j2user_id(cls, j):
        return j[cls.F.USER]

    @classmethod
    def j2thread_ts(cls, j):
        return j[cls.F.TS]