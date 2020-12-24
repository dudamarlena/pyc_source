# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/marvin.py
# Compiled at: 2011-04-22 06:35:42
"""
    complain like Marvin from the Hitchhiker's Guide to the Galaxy
"""
from otfbot.lib import chatMod
from otfbot.lib import functions
from otfbot.lib.pluginSupport.decorators import callback
import random

class Plugin(chatMod.chatMod):
    """ marvin plugin """

    def __init__(self, bot):
        self.bot = bot

    @callback
    def msg(self, user, channel, msg):
        """
            Let marvin complain with the propability specified in marvin.percent in the config
        """
        if (msg[0] == '!' or self.bot.nickname in msg) and len(self.marvin):
            number = random.randint(0, 100)
            chance = int(self.bot.config.get('percent', '1', 'marvin'))
            enc = self.bot.config.get('fileencoding', 'iso-8859-15', 'marvin')
            if number < chance:
                self.bot.sendmsg(channel, random.choice(self.marvin), enc)

    def start(self):
        """
            Loads the phrases from the data dir
        """
        fn = self.bot.config.getPath('file', datadir, 'marvin.txt', 'marvin')
        self.marvin = functions.loadList(fn)

    def reload(self):
        """
            Reloads the phrases from the datadir
        """
        self.start()