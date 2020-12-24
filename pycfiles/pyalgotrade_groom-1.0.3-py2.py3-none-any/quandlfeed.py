# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/barfeed/quandlfeed.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
from pyalgotrade.barfeed import csvfeed
from pyalgotrade import bar

class Feed(csvfeed.GenericBarFeed):
    """A :class:`pyalgotrade.barfeed.csvfeed.BarFeed` that loads bars from CSV files downloaded from Quandl.

    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** or **pyalgotrade.bar.Frequency.WEEK**
        are supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.

    .. note::
        When working with multiple instruments:

            * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.
            * If any of the instruments loaded are in different timezones, then the timezone parameter must be set.
    """

    def __init__(self, frequency=bar.Frequency.DAY, timezone=None, maxLen=None):
        if frequency not in [bar.Frequency.DAY, bar.Frequency.WEEK]:
            raise Exception('Invalid frequency.')
        super(Feed, self).__init__(frequency, timezone, maxLen)
        self.setDateTimeFormat('%Y-%m-%d')
        self.setColumnName('datetime', 'Date')
        self.setColumnName('adj_close', 'Adj. Close')