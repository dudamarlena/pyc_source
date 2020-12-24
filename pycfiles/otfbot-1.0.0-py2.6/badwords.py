# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/badwords.py
# Compiled at: 2011-04-22 06:35:42
"""
    Kick user from a channel based on a list of bad words
"""
from otfbot.lib import chatMod
from otfbot.lib import functions
from otfbot.lib.pluginSupport.decorators import callback
import re

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot

    def start(self):
        self.badwordsFile = self.bot.config.getPath('file', datadir, 'badwords.txt', 'badwords')
        self.register_ctl_command(self.reload)
        self.reload()

    def reload(self):
        """
            (Re-)load the file with the bad words
        """
        self.badwords = functions.loadList(self.badwordsFile)

    @callback
    def msg(self, user, channel, msg):
        nick = user.getNick()
        for word in self.badwords:
            if channel in self.bot.channels:
                if word != '' and re.search(word, msg, re.I):
                    self.logger.info('kicked %s for badword %s' % (nick, word))
                    self.bot.kick(channel, nick, 'Bad word: ' + word)