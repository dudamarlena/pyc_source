# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/ddate.py
# Compiled at: 2011-04-22 06:35:42
"""
    Calculate the discordian Date
"""
from otfbot.lib import chatMod
from otfbot.lib.pluginSupport.decorators import callback
import random, datetime, calendar
DISCORDIAN_SEASONS = [
 'Chaos', 'Discord', 'Confusion', 'Bureaucracy',
 'The Aftermath']
DISCORDIAN_WEEKDAYS = ['Sweetmorn', 'Boomtime', 'Pungenday', 'Prickle-Prickle',
 'Setting Orange']

def ddate(year, month, day, _):
    today = datetime.date(year, month, day)
    is_leap_year = calendar.isleap(year)
    if is_leap_year and month == 2 and day == 29:
        return "St. Tib's Day, YOLD " + (year + 1166)
    day_of_year = today.timetuple().tm_yday - 1
    weekday = day_of_year % 5
    if is_leap_year and day_of_year >= 60:
        day_of_year -= 1
    (season, dday) = divmod(day_of_year, 73)
    return _('Today is %s, the %d day of %s in the YOLD %d') % (
     DISCORDIAN_WEEKDAYS[weekday], dday + 1,
     DISCORDIAN_SEASONS[season], year + 1166)


class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot

    @callback
    def command(self, user, channel, command, options):
        _ = self.bot.get_gettext(channel)
        if command == 'ddate':
            dt = datetime.datetime.now()
            self.bot.sendmsg(channel, ddate(dt.year, dt.month, dt.day, _))