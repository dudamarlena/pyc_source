# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\technical\ratio.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 1411 bytes
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