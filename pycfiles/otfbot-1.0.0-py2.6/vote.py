# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/vote.py
# Compiled at: 2011-04-22 06:35:42
"""
cast a vote with !votecast question and collect answers
"""
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        self.bot.depends_on_service('scheduler')
        self.votes = {}

    @callback
    def command(self, user, channel, command, options):
        if command == 'newvote':
            if channel not in self.votes:
                self.votes[channel] = [
                 options, 0, 0, 0, []]
                self.bot.sendmsg(channel, 'Abstimmung: %s (!vote ja/nein/egal)' % options)
                self.bot.root.getServiceNamed('scheduler').callLater(60, self.voteend, channel)
            else:
                self.bot.sendmsg(channel, 'Es laeuft bereits eine Abstimmung.')
        elif command == 'vote':
            if channel not in self.votes:
                self.bot.sendmsg(channel, 'Es laeuft gerade keine Abstimmung')
                return
            if user in self.votes[channel][4]:
                self.bot.sendmsg(channel, '%s: Du hast schon abgestimmt!' % user.getNick())
            else:
                self.votes[channel][4].append(user)
                if options.lower() in ('yes', 'ja'):
                    self.votes[channel][1] += 1
                elif options.lower() in ('no', 'nein'):
                    self.votes[channel][2] += 1
                elif options.lower() in ('whatever', 'egal'):
                    self.votes[channel][3] += 1

    def voteend(self, channel):
        self.bot.sendmsg(channel, 'Vote: %s' % self.votes[channel][0])
        self.bot.sendmsg(channel, 'Ja: %s, Nein: %s, Egal: %s' % (self.votes[channel][1], self.votes[channel][2], self.votes[channel][3]))
        del self.votes[channel]