# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/barfeed/membf.py
# Compiled at: 2016-12-05 03:07:43
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import barfeed
from pyalgotrade import bar
from pyalgotrade import utils

class BarFeed(barfeed.BaseBarFeed):

    def __init__(self, frequency, maxLen=None):
        super(BarFeed, self).__init__(frequency, maxLen)
        self.__bars = {}
        self.__nextPos = {}
        self.__started = False
        self.__currDateTime = None
        return

    def reset(self):
        self.__nextPos = {}
        for instrument in self.__bars.keys():
            self.__nextPos.setdefault(instrument, 0)

        self.__currDateTime = None
        super(BarFeed, self).reset()
        return

    def getCurrentDateTime(self):
        return self.__currDateTime

    def start(self):
        super(BarFeed, self).start()
        self.__started = True

    def stop(self):
        pass

    def join(self):
        pass

    def addBarsFromSequence(self, instrument, bars):
        if self.__started:
            raise Exception("Can't add more bars once you started consuming bars")
        self.__bars.setdefault(instrument, [])
        self.__nextPos.setdefault(instrument, 0)
        self.__bars[instrument].extend(bars)
        barCmp = lambda x, y: cmp(x.getDateTime(), y.getDateTime())
        self.__bars[instrument].sort(barCmp)
        self.registerInstrument(instrument)

    def eof(self):
        ret = True
        for instrument, bars in self.__bars.iteritems():
            nextPos = self.__nextPos[instrument]
            if nextPos < len(bars):
                ret = False
                break

        return ret

    def peekDateTime(self):
        ret = None
        for instrument, bars in self.__bars.iteritems():
            nextPos = self.__nextPos[instrument]
            if nextPos < len(bars):
                ret = utils.safe_min(ret, bars[nextPos].getDateTime())

        return ret

    def getNextBars(self):
        smallestDateTime = self.peekDateTime()
        if smallestDateTime is None:
            return
        else:
            ret = {}
            for instrument, bars in self.__bars.iteritems():
                nextPos = self.__nextPos[instrument]
                if nextPos < len(bars) and bars[nextPos].getDateTime() == smallestDateTime:
                    ret[instrument] = bars[nextPos]
                    self.__nextPos[instrument] += 1

            if self.__currDateTime == smallestDateTime:
                raise Exception('Duplicate bars found for %s on %s' % (ret.keys(), smallestDateTime))
            self.__currDateTime = smallestDateTime
            return bar.Bars(ret)

    def loadAll(self):
        for dateTime, bars in self:
            pass