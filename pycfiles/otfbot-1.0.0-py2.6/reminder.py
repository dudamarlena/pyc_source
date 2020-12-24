# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/reminder.py
# Compiled at: 2011-04-22 06:35:42
import time
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback
from datetime import datetime

class Meta:
    service_depends = [
     'scheduler']


class Plugin(chatMod.chatMod):
    """ reminder plugin """

    def __init__(self, bot):
        self.bot = bot
        self.messages = {}
        self.bot.depends_on_service('scheduler', 'without scheduler the reminder-plugin cannot work')
        self.scheduler = self.bot.root.getServiceNamed('scheduler')

    @callback
    def remind(self, user, channel, message):
        """
            called at every time where a reminder is set.
            will send all reminders at given time to the appropriate channels.
        """
        self.bot.sendmsg(channel, user + ': Reminder: ' + message)

    @callback
    def command(self, user, channel, command, options):
        """
            react on !remindme 

            add new reminders with !remindme (float) (string), i.e. !remindme 5.0 coffee is ready
        """
        _ = self.bot.get_gettext(channel)
        user = user.getNick()
        if command == 'remindmein':
            options = options.split(' ', 1)
            if not len(options) == 2:
                self.bot.sendmsg(channel, user + _(': ERROR: You need to specify a number of minutes and a reminder text!'))
                return
            try:
                wait = float(options[0])
            except ValueError:
                self.bot.sendmsg(channel, user + _(': ERROR: invalid number format "%s".') % options[0])
                return
            else:
                text = str(options[1])
                self.bot.sendmsg(channel, user + _(': I will remind you in %i minutes') % wait)
                self.scheduler.callLater(wait * 60, self.remind, user, channel, text)
        if command == 'remindmeat':
            options = options.split(' ', 2)
            if len(options) == 3 and len(options[0].split('-')) == 3 and len(options[1].split(':')) == 2:
                rdate = options[0].split('-')
                rtime = options[1].split(':')
                try:
                    dt = datetime(int(rdate[0]), int(rdate[1]), int(rdate[2]), int(rtime[0]), int(rtime[1]))
                except ValueError:
                    self.bot.sendmsg(channel, user + _(': Syntax: !remindmeat YYYY-MM-DD hh:mm <reminder text>'))
                    return
                else:
                    text = str(options[2])
                    if self.scheduler.callAtDatetime(dt, self.remind, user, channel, text) != False:
                        self.bot.sendmsg(channel, user + _(': I will remind you at %s %s') % (options[0], options[1]))
                    else:
                        self.bot.sendmsg(channel, user + _(': ERROR: You specified a date in the past'))
            else:
                self.bot.sendmsg(channel, user + _(': Syntax: !remindmeat YYYY-MM-DD hh:mm <reminder text>'))