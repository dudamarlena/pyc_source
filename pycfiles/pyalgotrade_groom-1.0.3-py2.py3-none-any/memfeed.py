# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/feed/memfeed.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
from pyalgotrade import feed
from pyalgotrade import dataseries

class MemFeed(feed.BaseFeed):

    def __init__(self, maxLen=None):
        super(MemFeed, self).__init__(maxLen)
        self.__values = []
        self.__nextIdx = 0

    def reset(self):
        self.__nextIdx = 0
        feed.BaseFeed.reset(self)

    def start(self):
        super(MemFeed, self).start()
        cmpFun = lambda x, y: cmp(x[0], y[0])
        self.__values.sort(cmpFun)

    def stop(self):
        pass

    def join(self):
        pass

    def eof(self):
        if self.__nextIdx < len(self.__values):
            return False
        else:
            return True

    def peekDateTime(self):
        ret = None
        if self.__nextIdx < len(self.__values):
            ret = self.__values[self.__nextIdx][0]
        return ret

    def createDataSeries(self, key, maxLen):
        return dataseries.SequenceDataSeries(maxLen)

    def getNextValues(self):
        ret = (None, None)
        if self.__nextIdx < len(self.__values):
            ret = self.__values[self.__nextIdx]
            self.__nextIdx += 1
        return ret

    def addValues(self, values):
        for key in values[0][1].keys():
            self.registerDataSeries(key)

        self.__values.extend(values)