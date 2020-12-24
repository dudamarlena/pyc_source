# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/eightBall.py
# Compiled at: 2011-04-22 06:35:42
"""
    Provide some aid to make a decision
"""
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback
import random, re

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        _ = self.bot.get_gettext()
        self.answers = [
         _('Signs point to yes'),
         _('Yes'),
         _('Without a doubt'),
         _('As I see it, yes'),
         _('Most likely'),
         _('You may rely on it'),
         _('Yes definitely'),
         _('It is decidedly so'),
         _('Outlook good'),
         _('It is certain'),
         _('My sources say no'),
         _('Very doubtful'),
         _("Don't count on it"),
         _('Outlook not so good'),
         _('My reply is no'),
         _('Reply hazy, try again'),
         _('Concentrate and ask again'),
         _('Better not tell you now'),
         _('Cannot predict now'),
         _('Ask again later')]

    @callback
    def msg(self, user, channel, msg):
        if self.bot.config.getBool('autoAnswer', False, 'eightball', self.network, channel):
            if re.match('[a-z][^\\.\\?!:;]*\\?', msg.lower()):
                self.bot.sendmsg(channel, random.choice(self.answers))

    @callback
    def command(self, user, channel, command, options):
        if command.lower() in ('8ball', 'eightball') and options != '':
            self.bot.sendmsg(channel, random.choice(self.answers))