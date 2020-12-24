# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/identify.py
# Compiled at: 2011-04-22 06:35:42
"""
Identify the Bot to a nickserv, if the botnick is registered
"""
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        self.sent_identification = False

    @callback
    def signedOn(self):
        self.identify()

    def identify(self):
        password = self.bot.config.get('nickservPassword', None, 'identify', self.bot.network)
        if password:
            self.logger.info('identifying to nickserv')
            self.bot.sendmsg('nickserv', 'identify ' + password)
            self.sent_identification = True
        if self.bot.config.getBool('setBotFlag', True, 'identify', self.bot.network):
            self.logger.info('setting usermode +b')
            self.bot.mode(self.bot.nickname, 1, 'B')
        return

    @callback
    def noticed(self, user, channel, msg):
        user = user.getNick()
        if user.lower() == 'nickserv' and self.sent_identification:
            self.logger.debug(user + ': ' + msg)

    @callback
    def connectionLost(self, reason):
        self.sent_identification = False