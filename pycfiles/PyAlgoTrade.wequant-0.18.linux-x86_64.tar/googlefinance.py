# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/tools/googlefinance.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
.. moduleauthor:: Maciej Żok <maciek.zok@gmail.com>
"""
import os, datetime, pyalgotrade.logger
from pyalgotrade import bar
from pyalgotrade.barfeed import googlefeed
from pyalgotrade.utils import csvutils

def download_csv(instrument, begin, end):
    url = 'http://www.google.com/finance/historical'
    params = {'q': instrument, 
       'startdate': begin.strftime('%Y-%m-%d'), 
       'enddate': end.strftime('%Y-%m-%d'), 
       'output': 'csv'}
    return csvutils.download_csv(url, url_params=params, content_type='application/vnd.ms-excel')


def download_daily_bars(instrument, year, csvFile):
    """Download daily bars from Google Finance for a given year.

    :param instrument: Instrument identifier.
    :type instrument: string.
    :param year: The year.
    :type year: int.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.
    """
    bars = download_csv(instrument, datetime.date(year, 1, 1), datetime.date(year, 12, 31))
    f = open(csvFile, 'w')
    f.write(bars)
    f.close()


def build_feed(instruments, fromYear, toYear, storage, frequency=bar.Frequency.DAY, timezone=None, skipErrors=False):
    """Build and load a :class:`pyalgotrade.barfeed.googlefeed.Feed` using CSV files downloaded from Google Finance.
    CSV files are downloaded if they haven't been downloaded before.

    :param instruments: Instrument identifiers.
    :type instruments: list.
    :param fromYear: The first year.
    :type fromYear: int.
    :param toYear: The last year.
    :type toYear: int.
    :param storage: The path were the files will be loaded from, or downloaded to.
    :type storage: string.
    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** is currently supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param skipErrors: True to keep on loading/downloading files in case of errors.
    :type skipErrors: boolean.
    :rtype: :class:`pyalgotrade.barfeed.googlefeed.Feed`.
    """
    logger = pyalgotrade.logger.getLogger('googlefinance')
    ret = googlefeed.Feed(frequency, timezone)
    if not os.path.exists(storage):
        logger.info(('Creating {dirname} directory').format(dirname=storage))
        os.mkdir(storage)
    for year in range(fromYear, toYear + 1):
        for instrument in instruments:
            fileName = os.path.join(storage, ('{instrument}-{year}-googlefinance.csv').format(instrument=instrument, year=year))
            if not os.path.exists(fileName):
                logger.info(('Downloading {instrument} {year} to {filename}').format(instrument=instrument, year=year, filename=fileName))
                try:
                    if frequency == bar.Frequency.DAY:
                        download_daily_bars(instrument, year, fileName)
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