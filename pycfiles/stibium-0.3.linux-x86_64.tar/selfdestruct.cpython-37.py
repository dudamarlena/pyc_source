# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/stibium/contrib/selfdestruct.py
# Compiled at: 2019-09-02 08:41:04
# Size of source mod 2**32: 792 bytes
"""This module provides the SelfDestructMessage class"""
from ..handlers import TimeoutHandler
from ..dataclasses import Message

class SelfDestructMessage(TimeoutHandler):
    __doc__ = '\n    Self-destructing message handler\n\n    This handler will automatically remove ("unsend")\n    a message after a set timeout.\n    '
    mid = None

    def __init__(self, mid, timeout):
        super().__init__(handler=None, timeout=timeout)
        self.mid = mid

    def setup(self, bot):
        if self.mid is None:
            raise Exception(f"MID for {type(self).__name__} not provided")
        elif isinstance(self.mid, Message):
            self.mid = self.mid.mid
        else:
            self.mid = str(self.mid)

    def handlerfn(self, event, bot):
        bot.fbchat_client.unsend(mid=(self.mid))