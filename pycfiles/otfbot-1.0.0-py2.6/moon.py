# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/moon.py
# Compiled at: 2011-04-22 06:35:42
"""
    Calculate the current phase of the moon
"""
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback
import time

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot

    @callback
    def command(self, user, channel, command, options):
        _ = self.bot.get_gettext(channel)
        known_fullmoon_date = 915245340
        monthlength = 29.530588
        ts = time.time()
        if command in ('moon', 'fullmoon', 'mond', 'vollmond'):
            if len(options):
                options = options.split('-')
                if len(options) == 3:
                    try:
                        year = int(options[0])
                        month = int(options[1])
                        day = int(options[2])
                        ts = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
                    except ValueError:
                        self.bot.sendmsg(channel, _('Time format: XXXX-XX-XX'))
                        return

                else:
                    self.bot.sendmsg(channel, _('Time format: XXXX-XX-XX'))
                    return
        phase = (ts - known_fullmoon_date) / 86400 / monthlength
        phase = phase - int(phase)
        if command == 'fullmoon' or command == 'vollmond':
            self.bot.sendmsg(channel, _('Next fullmoon in %d days') % round((1 - phase) * monthlength))
        elif command == 'moon' or command == 'mond':
            symbol = ''
            name = ''
            if phase < 0.05:
                symbol = '[ (  ) ]'
                name = _('fullmoon')
            elif phase < 0.2:
                symbol = '[ C   ]'
                name = _('decreasing moon')
            elif phase < 0.3:
                symbol = '[ C   ]'
                name = _('half moon')
            elif phase < 0.45:
                symbol = '[ (   ]'
                name = _('decreasing moon')
            elif phase < 0.65:
                symbol = '[     ]'
                name = _('new moon')
            elif phase < 0.8:
                symbol = '[   ) ]'
                name = _('waxing moon')
            elif phase < 0.8:
                symbol = '[   D ]'
                name = _('half moon')
            else:
                symbol = '[   D ]'
                name = _('waxing moon')
            self.bot.sendmsg(channel, '%s %s' % (symbol, name))