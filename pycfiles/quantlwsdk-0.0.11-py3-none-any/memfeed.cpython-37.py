# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\feed\memfeed.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 2247 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import feed
from pyalgotrade import dataseries

class MemFeed(feed.BaseFeed):

    def __init__(self, maxLen=None):
        super(MemFeed, self).__init__(maxLen)
        self._MemFeed__values = []
        self._MemFeed__nextIdx = 0

    def reset(self):
        self._MemFeed__nextIdx = 0
        feed.BaseFeed.reset(self)

    def start(self):
        super(MemFeed, self).start()
        self._MemFeed__values.sort(key=(lambda x: x[0]))

    def stop(self):
        pass

    def join(self):
        pass

    def eof(self):
        if self._MemFeed__nextIdx < len(self._MemFeed__values):
            return False
        return True

    def peekDateTime(self):
        ret = None
        if self._MemFeed__nextIdx < len(self._MemFeed__values):
            ret = self._MemFeed__values[self._MemFeed__nextIdx][0]
        return ret

    def createDataSeries(self, key, maxLen):
        return dataseries.SequenceDataSeries(maxLen)

    def getNextValues(self):
        ret = (None, None)
        if self._MemFeed__nextIdx < len(self._MemFeed__values):
            ret = self._MemFeed__values[self._MemFeed__nextIdx]
            self._MemFeed__nextIdx += 1
        return ret

    def addValues(self, values):
        for key in values[0][1].keys():
            self.registerDataSeries(key)

        self._MemFeed__values.extend(values)