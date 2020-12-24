# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/tools/yahoofinance.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import os, datetime, pyalgotrade.logger
from pyalgotrade import bar
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.utils import dt
from pyalgotrade.utils import csvutils

def __adjust_month(month):
    if month > 12 or month < 1:
        raise Exception('Invalid month')
    month -= 1
    return month


def download_csv(instrument, begin, end, frequency):
    url = 'http://ichart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=%s&ignore=.csv' % (instrument, __adjust_month(begin.month), begin.day, begin.year, __adjust_month(end.month), end.day, end.year, frequency)
    return csvutils.download_csv(url)


def download_daily_bars(instrument, year, csvFile):
    """Download daily bars from Yahoo! Finance for a given year.

    :param instrument: Instrument identifier.
    :type instrument: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    """
    bars = download_csv(instrument, datetime.date(year, 1, 1), datetime.date(year, 12, 31), 'd')
    f = open(csvFile, 'w')
    f.write(bars)
    f.close()


def download_weekly_bars(instrument, year, csvFile):
    """Download weekly bars from Yahoo! Finance for a given year.

    :param instrument: Instrument identifier.
    :type instrument: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    """
    begin = dt.get_first_monday(year)
    end = dt.get_last_monday(year) + datetime.timedelta(days=6)
    bars = download_csv(instrument, begin, end, 'w')
    f = open(csvFile, 'w')
    f.write(bars)
    f.close()


def build_feed(instruments, fromYear, toYear, storage, frequency=bar.Frequency.DAY, timezone=None, skipErrors=False):
    """Build and load a :class:`pyalgotrade.barfeed.yahoofeed.Feed` using CSV files downloaded from Yahoo! Finance.
    CSV files are downloaded if they haven't been downloaded before.

    :param instruments: Instrument identifiers.
    :type instruments: list.
    :param fromYear: The first year.
    :type fromYear: int.
    :param toYear: The last year.
    :type toYear: int.
    :param storage: The path were the files will be loaded from, or downloaded to.
    :type storage: string.
    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** or **pyalgotrade.bar.Frequency.WEEK**
        are supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param skipErrors: True to keep on loading/downloading files in case of errors.
    :type skipErrors: boolean.
    :rtype: :class:`pyalgotrade.barfeed.yahoofeed.Feed`.
    """
    logger = pyalgotrade.logger.getLogger('yahoofinance')
    ret = yahoofeed.Feed(frequency, timezone)
    if not os.path.exists(storage):
        logger.info('Creating %s directory' % storage)
        os.mkdir(storage)
    for year in range(fromYear, toYear + 1):
        for instrument in instruments:
            fileName = os.path.join(storage, '%s-%d-yahoofinance.csv' % (instrument, year))
            if not os.path.exists(fileName):
                logger.info('Downloading %s %d to %s' % (instrument, year, fileName))
                try:
                    if frequency == bar.Frequency.DAY:
                        download_daily_bars(instrument, year, fileName)
                    elif frequency == bar.Frequency.WEEK:
                        download_weekly_bars(instrument, year, fileName)
                    else:
                        raise Exception('Invalid frequency')
                except Exception as e:
                    if skipErrors:
                        logger.error(str(e))
                        continue
                    else:
                        raise e

            ret.addBarsFromCSV(instrument, fileName)

    return ret