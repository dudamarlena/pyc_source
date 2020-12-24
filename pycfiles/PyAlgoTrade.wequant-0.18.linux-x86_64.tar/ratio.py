# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/ratio.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
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