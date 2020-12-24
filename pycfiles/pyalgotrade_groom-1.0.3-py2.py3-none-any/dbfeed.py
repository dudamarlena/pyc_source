# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/barfeed/dbfeed.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'

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