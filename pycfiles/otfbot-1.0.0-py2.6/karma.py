# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/karma.py
# Compiled at: 2011-04-22 06:35:42
"""
    Track the karma of user supplied terms
"""
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback
import pickle, os

def sortedbyvalue(dict):
    """Helper function to return a [(value, key)] list from a dict"""
    items = [ (k, v) for (v, k) in dict.items() ]
    items.reverse()
    return items


class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        self.karmas = {}
        self.karmapaths = {}
        self.verbose = self.bot.config.getBool('karma.verbose', True)
        self.freestyle = self.bot.config.getBool('karma.freestyle', True)

    def loadKarma(self, channel):
        if not os.path.exists(datadir):
            os.makedirs(datadir)
        karmapath = self.bot.config.getPath('file', datadir, 'karma.dat', 'karma', self.bot.network, channel)
        if karmapath not in self.karmapaths.keys():
            if os.path.exists(karmapath):
                karmafile = open(karmapath, 'r')
                self.karmas[channel] = pickle.load(karmafile)
                self.karmapaths[karmapath] = channel
                karmafile.close()
            else:
                self.karmas[channel] = {}
        else:
            self.karmas[channel] = self.karmas[self.karmapaths[karmapath]]

    def saveKarma(self, channel):
        karmapath = self.bot.config.getPath('file', datadir, 'karma.dat', 'karma', self.bot.network, channel)
        karmafile = open(karmapath, 'w')
        pickle.dump(self.karmas[channel], karmafile)
        karmafile.close()

    @callback
    def joined(self, channel):
        self.loadKarma(channel)

    @callback
    def left(self, channel):
        self.saveKarma(channel)

    @callback
    def command(self, user, channel, command, options):
        up = False
        what = None
        reason = None
        num_reasons = 5
        num_user = 5
        tmp = options.split('#', 1)
        options = tmp[0].strip()
        if len(tmp) == 2:
            reason = tmp[1]
        if command == 'karma':
            if options == '':
                rmsg = 'Nutzen: !karma name++ oder !karma name--'
                self.bot.sendmsg(channel, rmsg)
                return
            if options[-2:] == '++':
                up = True
                what = options[:-2]
            elif options[-2:] == '--':
                up = False
                what = options[:-2]
            else:
                self.tell_karma(options, channel)
                return
            self.do_karma(channel, what, up, reason, user)
            if self.verbose:
                self.tell_karma(what, channel)
        elif command == 'why-karmaup' or command == 'wku':
            options.strip()
            reasons = ''
            if options in self.karma.keys():
                num = min(num_reasons, len(self.karma[options][3]))
                while num > 0:
                    num -= 1
                    reasons += ' .. ' + self.karma[options][3][(-num)]

                reasons = reasons[4:]
                self.bot.sendmsg(channel, reasons)
        elif command == 'why-karmadown' or command == 'wkd':
            options.strip()
            reasons = ''
            if options in self.karma.keys():
                num = min(num_reasons, len(self.karma[options][4]))
                while num > 0:
                    num -= 1
                    reasons += ' .. ' + self.karma[options][4][(-num)]

                reasons = reasons[4:]
                self.bot.sendmsg(channel, reasons)
        elif command == 'who-karmaup':
            options.strip()
            people = ''
            if options in self.karma.keys():
                items = sortedbyvalue(self.karma[options][1])
                num = min(num_user, len(items))
                while num > 0:
                    num -= 1
                    people += ' .. ' + items[(-num)][1] + '=' + str(items[(-num)][0])

                people = people[4:]
                self.bot.sendmsg(channel, people)
        elif command == 'who-karmadown':
            options.strip()
            people = ''
            if options in self.karma.keys():
                items = sortedbyvalue(self.karma[options][2])
                num = min(num_user, len(items))
                while num > 0:
                    num -= 1
                    people += ' .. ' + items[(-num)][1] + '=' + str(items[(-num)][0])

                people = people[4:]
                self.bot.sendmsg(channel, people)
        elif self.freestyle:
            if options[-2:] == '++':
                up = True
                what = command + ' ' + options[:-2]
            elif options[-2:] == '--':
                up = False
                what = command + ' ' + options[:-2]
            elif command[-2:] == '++':
                up = True
                what = command[:-2]
            elif command[-2:] == '--':
                up = False
                what = command[:-2]
            if what:
                self.do_karma(channel, what, up, reason, user)
                if self.verbose:
                    self.tell_karma(what, channel)
        return

    def tell_karma(self, what, channel):
        self.bot.sendmsg(channel, 'Karma: ' + what + ': ' + str(self.get_karma(channel, what)))

    def get_karma(self, channel, what):
        if what not in self.karmas[channel].keys():
            self.karmas[channel][what] = [
             0, {}, {}, [], []]
        return self.karmas[channel][what][0]

    def do_karma(self, channel, what, up, reason, user):
        user = user.getNick()
        karma = self.karmas[channel]
        if what not in karma.keys():
            karma[what] = [0, {}, {}, [], []]
        if up:
            karma[what][0] = int(karma[what][0]) + 1
            if user not in karma[what][1].keys():
                karma[what][1][user] = 1
            else:
                karma[what][1][user] += 1
            if reason:
                karma[what][3].append(str(reason))
        else:
            karma[what][0] = int(karma[what][0]) - 1
            if user not in karma[what][2].keys():
                karma[what][2][user] = 1
            else:
                karma[what][2][user] += 1
            if reason:
                karma[what][4].append(str(reason))

    def stop(self):
        for karmapath in self.karmapaths.keys():
            self.saveKarma(self.karmapaths[karmapath])

    def start(self):
        for c in self.bot.channels:
            self.joined(c)