# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/plugins/ircClient/statistics.py
# Compiled at: 2011-04-22 06:35:42
"""
    Calculate some statistics, like peak usercount.
"""
import time
from otfbot.lib import chatMod
from otfbot.lib import functions
from otfbot.lib.pluginSupport.decorators import callback

class Plugin(chatMod.chatMod):

    def __init__(self, bot):
        self.bot = bot
        self.peak = {}
        self.peak_date = {}
        self.linesperminute = {}
        self.new_lines = {}
        self.timestamp = {}

    @callback
    def msg(self, user, channel, msg):
        self.calcLPM(channel)
        self.new_lines[channel][(-1)] += 1

    def calcLPM(self, channel):
        new_timestamp = int(time.time())
        if channel not in self.timestamp:
            self.timestamp[channel] = new_timestamp
        if channel not in self.new_lines:
            self.new_lines[channel] = [
             0, 0, 0, 0, 0]
        no_lines = reduce(lambda x, y: x + y, self.new_lines[channel][:-1])
        timediff = new_timestamp - self.timestamp[channel]
        if timediff > 0:
            self.linesperminute[channel] = no_lines * 60 / 4.0 / timediff
        if timediff >= 60:
            self.new_lines[channel] = self.new_lines[channel][1:]
            self.new_lines[channel].append(0)
            self.timestamp[channel] = new_timestamp

    def getLinesPerMinute(self, channel):
        self.calcLPM(channel)
        if channel not in self.linesperminute:
            self.linesperminute[channel] = 0
        return self.linesperminute[channel]

    @callback
    def joined(self, channel):
        if channel not in self.peak:
            self.peak[channel] = len(self.bot.getUsers(channel))
        if channel not in self.peak_date:
            self.peak_date[channel] = time.strftime('%d.%m.%Y %H:%M')
        self._recalc_peak(channel)

    @callback
    def userJoined(self, user, channel):
        self._recalc_peak(channel)

    def _recalc_peak(self, channel):
        if channel not in self.peak:
            self.peak[channel] = len(self.bot.getUsers(channel))
        if self.peak[channel] < len(self.bot.getUsers(channel)):
            self.peak[channel] = len(self.bot.getUsers(channel))
            self.peak_date[channel] = time.strftime('%d.%m.%Y %H:%M')

    @callback
    def command(self, user, channel, command, options):
        if command == 'peak':
            self.bot.sendmsg(channel, 'Maximale Nutzerzahl (%s) erreicht am %s' % (self.peak[channel], self.peak_date[channel]))
        elif command == 'lpm':
            self.bot.sendmsg(channel, 'aktuelle Zeilen pro Minute: %s' % self.getLinesPerMinute(channel))