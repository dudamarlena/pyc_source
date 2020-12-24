# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/version.py
# Compiled at: 2011-04-22 06:35:42
from otfbot.lib import chatMod
from otfbot.lib.vername import *
from otfbot.lib.pluginSupport.decorators import callback

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot

    @callback
    def command(self, user, channel, command, options):
        if command == 'version':
            self.bot.sendmsg(channel, self.bot.root.version.short())
        elif command == 'ver2name':
            if not len(options) == 7:
                self.bot.sendmsg(channel, 'need 7-digit version')
            elif not set(options).issubset(set(hex)):
                self.bot.sendmsg(channel, 'git versions are 7 digits [0-9a-f]')
            else:
                self.bot.sendmsg(channel, ver2name(options))
        elif command == 'name2ver':
            options = options.lower()
            if not len(options) == 9:
                self.bot.sendmsg(channel, 'need 9-character version name')
            elif not validVername(options):
                self.bot.sendmsg(channel, 'invalid version name')
            else:
                self.bot.sendmsg(channel, name2ver(options))