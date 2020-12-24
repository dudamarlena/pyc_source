# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/contrib/everyone.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 1586 bytes
"""This module provides the EveryoneCommand class"""
from fbchat import models
from ..dataclasses import Thread
from ..handlers import CommandHandler

class EveryoneCommand(CommandHandler):
    __doc__ = '\n    "Everyone" command.\n\n    This handler creates a command, which tags everyone\n    present in the group. It can be used to demand attention\n    from the whole group, for example for important announcements.\n    Take note not to overuse it, as it can be annoying.\n    TODO: create a permissions system, which could be paired with this command\n    '
    group = None
    uids = []

    def __init__(self, group, command='everyone'):
        super().__init__(handler=None, command=command)
        self.group = Thread.from_group_uid(group)

    def check(self, event, bot):
        if event.thread != self.group:
            return False
        return super().check(event, bot)

    def handlerfn(self, message, bot):
        if not self.uids:
            self.uids = bot.fbchat_client.fetchGroupInfo(self.group.id_)[self.group.id_].participants
        alphabet = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        out = ''
        offset = 0
        mentions = []
        for i in self.uids:
            mentions.append(models.Mention(i, offset=offset, length=2))
            out = out + '@' + alphabet[(offset // 3)] + ' '
            offset += 3

        bot.fbchat_client.send(models.Message(text=out, mentions=mentions),
          thread_type=(self.group.type_),
          thread_id=(self.group.id_))