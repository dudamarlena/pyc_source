# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/seen.py
# Compiled at: 2011-04-22 06:35:42
import pickle, time, os
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        try:
            os.mkdir(datadir)
        except OSError:
            pass

        try:
            f = file(datadir + '/users', 'rb')
            self.userdata = pickle.load(f)
            f.close()
        except IOError:
            self.userdata = [{}]

        self.bot.root.getServiceNamed('scheduler').callPeriodic(60, self.save_data)

    @callback
    def joined(self, channel):
        try:
            self.userdata[0][channel]
        except KeyError:
            self.userdata[0][channel] = {}

    @callback
    def msg(self, user, channel, msg):
        if channel[0] == '#':
            self.userdata[0][channel][user.getNick().lower()] = {'msg': msg, 'time': time.time()}

    @callback
    def command(self, user, channel, command, options):
        if command in ('seen', 'seen-exact'):
            user = self.bot.getUserByNick(options)
            if user and user.hasChannel(channel):
                self.bot.sendmsg(channel, '%s is in the channel!' % options)
            elif options.lower() in self.userdata[0][channel]:
                zeit = self.userdata[0][channel][options.lower()]['time']
                msg = self.userdata[0][channel][options.lower()]['msg']
                if command == 'seen-exact':
                    self.bot.sendmsg(channel, 'user ' + options + ' was last seen on ' + str(time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime(zeit))) + " saying '" + msg + "'.")
                else:
                    delta = int(time.time() - zeit)
                    days = delta / 86400
                    delta = delta % 86400
                    hours = delta / 3600
                    delta = delta % 3600
                    minutes = delta / 60
                    seconds = delta % 60
                    if days > 0:
                        self.bot.sendmsg(channel, 'user ' + options + ' was last seen %d days and %d hours ago, saying "%s" ' % (
                         days, hours, msg))
                    elif hours > 0:
                        self.bot.sendmsg(channel, 'user ' + options + ' was last seen %d hours and %d minutes ago, saying "%s" ' % (
                         hours, minutes, msg))
                    elif minutes > 0:
                        self.bot.sendmsg(channel, 'user ' + options + ' was last seen %d minutes and %d seconds ago, saying "%s" ' % (
                         minutes, seconds, msg))
                    else:
                        self.bot.sendmsg(channel, 'user ' + options + ' just left %d seconds ago, saying "%s"' % (
                         seconds, msg))
            else:
                self.bot.sendmsg(channel, 'user ' + options + ' is unknown')

    def stop(self):
        self.save_data()

    def save_data(self):
        f = file(datadir + '/users', 'wb')
        pickle.dump(self.userdata, f)
        f.close()