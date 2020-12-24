# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\barfeed\dbfeed.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 1283 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

class Database(object):

    def addBars(self, bars, frequency):
        for instrument in bars.getInstruments():
            bar = bars.getBar(instrument)
            self.addBar(instrument, bar, frequency)

    def addBarsFromFeed(self, feed):
        for dateTime, bars in feed:
            if bars:
                self.addBars(bars, feed.getFrequency())

    def addBar(self, instrument, bar, frequency):
        raise NotImplementedError()

    def getBars(self, instrument, frequency, timezone=None, fromDateTime=None, toDateTime=None):
        raise NotImplementedError()