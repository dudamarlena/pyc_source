# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\../gm3\indicatorModule\pyalgotrade\barfeed\quandlfeed.py
# Compiled at: 2019-06-05 03:25:53
# Size of source mod 2**32: 2264 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade.barfeed import csvfeed
from pyalgotrade import bar

class Feed(csvfeed.GenericBarFeed):
    __doc__ = 'A :class:`pyalgotrade.barfeed.csvfeed.BarFeed` that loads bars from CSV files downloaded from Quandl.\n\n    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** or **pyalgotrade.bar.Frequency.WEEK**\n        are supported.\n    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.\n    :type timezone: A pytz timezone.\n    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.\n        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the\n        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.\n    :type maxLen: int.\n\n    .. note::\n        When working with multiple instruments:\n\n            * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.\n            * If any of the instruments loaded are in different timezones, then the timezone parameter must be set.\n    '

    def __init__(self, frequency=bar.Frequency.DAY, timezone=None, maxLen=None):
        if frequency not in [bar.Frequency.DAY, bar.Frequency.WEEK]:
            raise Exception('Invalid frequency')
        super(Feed, self).__init__(frequency, timezone, maxLen)
        self.setDateTimeFormat('%Y-%m-%d')
        self.setColumnName('datetime', 'Date')
        self.setColumnName('adj_close', 'Adj. Close')