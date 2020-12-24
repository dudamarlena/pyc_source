# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/contrib/selfdestruct.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 792 bytes
__doc__ = 'This module provides the SelfDestructMessage class'
from ..handlers import TimeoutHandler
from ..dataclasses import Message

class SelfDestructMessage(TimeoutHandler):
    """SelfDestructMessage"""
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