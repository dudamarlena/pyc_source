# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/ratio.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
from pyalgotrade import technical
from pyalgotrade import utils

class RatioEventWindow(technical.EventWindow):

    def __init__(self):
        super(RatioEventWindow, self).__init__(2)

    def getValue(self):
        ret = None
        if self.windowFull():
            prev = self.getValues()[0]
            actual = self.getValues()[(-1)]
            ret = utils.get_change_percentage(actual, prev)
        return ret


class Ratio(technical.EventBasedFilter):

    def __init__(self, dataSeries, maxLen=None):
        super(Ratio, self).__init__(dataSeries, RatioEventWindow(), maxLen)