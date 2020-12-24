# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\../gm3\indicatorModule\pyalgotrade\barfeed\membf.py
# Compiled at: 2019-06-05 03:25:53
# Size of source mod 2**32: 3698 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import six
from pyalgotrade import barfeed
from pyalgotrade import bar
from pyalgotrade import utils

class BarFeed(barfeed.BaseBarFeed):

    def __init__(self, frequency, maxLen=None):
        super(BarFeed, self).__init__(frequency, maxLen)
        self._BarFeed__bars = {}
        self._BarFeed__nextPos = {}
        self._BarFeed__started = False
        self._BarFeed__currDateTime = None

    def reset(self):
        self._BarFeed__nextPos = {}
        for instrument in self._BarFeed__bars.keys():
            self._BarFeed__nextPos.setdefault(instrument, 0)

        self._BarFeed__currDateTime = None
        super(BarFeed, self).reset()

    def getCurrentDateTime(self):
        return self._BarFeed__currDateTime

    def start(self):
        super(BarFeed, self).start()
        self._BarFeed__started = True

    def stop(self):
        pass

    def join(self):
        pass

    def addBarsFromSequence(self, instrument, bars):
        if self._BarFeed__started:
            raise Exception("Can't add more bars once you started consuming bars")
        self._BarFeed__bars.setdefault(instrument, [])
        self._BarFeed__nextPos.setdefault(instrument, 0)
        self._BarFeed__bars[instrument].extend(bars)
        self._BarFeed__bars[instrument].sort(key=(lambda b: b.getDateTime()))
        self.registerInstrument(instrument)

    def eof(self):
        ret = True
        for instrument, bars in six.iteritems(self._BarFeed__bars):
            nextPos = self._BarFeed__nextPos[instrument]
            if nextPos < len(bars):
                ret = False
                break

        return ret

    def peekDateTime(self):
        ret = None
        for instrument, bars in six.iteritems(self._BarFeed__bars):
            nextPos = self._BarFeed__nextPos[instrument]
            if nextPos < len(bars):
                ret = utils.safe_min(ret, bars[nextPos].getDateTime())

        return ret

    def getNextBars(self):
        smallestDateTime = self.peekDateTime()
        if smallestDateTime is None:
            return
        ret = {}
        for instrument, bars in six.iteritems(self._BarFeed__bars):
            nextPos = self._BarFeed__nextPos[instrument]
            if nextPos < len(bars) and bars[nextPos].getDateTime() == smallestDateTime:
                ret[instrument] = bars[nextPos]
                self._BarFeed__nextPos[instrument] += 1

        if self._BarFeed__currDateTime == smallestDateTime:
            raise Exception('Duplicate bars found for %s on %s' % (list(ret.keys()), smallestDateTime))
        self._BarFeed__currDateTime = smallestDateTime
        return bar.Bars(ret)

    def loadAll(self):
        for dateTime, bars in self:
            pass