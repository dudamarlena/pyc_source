# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/timediff.py
# Compiled at: 2011-04-22 06:35:42
"""
    provide time and compare CTCP times
"""
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback
from time import mktime, ctime, strptime, time, sleep

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        self.queries = {}
        self.compare = {}

    @callback
    def command(self, user, channel, command, options):
        _ = self.bot.get_gettext(channel)
        if command == 'time':
            self.bot.sendmsg(channel, _('my time: %s') % ctime())
        elif command == 'timediff':
            self.bot.ctcpMakeQuery(user.getNick(), [('TIME', None)])
            self.queries[user] = channel
        return

    @callback
    def ctcpReply(self, user, channel, tag, data):
        if tag == 'TIME':
            if user in self.queries:
                try:
                    _ = self.bot.get_gettext(self.queries[user])
                    timediff = time() - mktime(strptime(data))
                    self.bot.sendmsg(self.queries[user], _('my time: %s, your time: %s, %d seconds difference') % (
                     ctime(), data, timediff))
                except ValueError:
                    pass
                else:
                    del self.queries[user]