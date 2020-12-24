# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/barfeed/dbfeed.py
# Compiled at: 2016-11-29 01:45:48
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