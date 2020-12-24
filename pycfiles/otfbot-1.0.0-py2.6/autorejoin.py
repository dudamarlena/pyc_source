# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/autorejoin.py
# Compiled at: 2011-04-22 06:35:42
"""
Rejoin, if kicked. (note: this is often a bad idea!)
"""
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot

    @callback
    def kickedFrom(self, channel, kicker, message):
        if int(self.bot.config.get('enabled', False, 'autorejoin', self.bot.network, channel)):
            self.bot.join(channel)