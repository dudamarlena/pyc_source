# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/tools/resample.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import os
from pyalgotrade import dispatcher
from pyalgotrade.dataseries import resampled
datetime_format = '%Y-%m-%d %H:%M:%S'

class CSVFileWriter(object):

    def __init__(self, csvFile):
        self.__file = open(csvFile, 'w')
        self.__writeLine('Date Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close')

    def __writeLine(self, *values):
        line = (',').join([ str(value) for value in values ])
        self.__file.write(line)
        self.__file.write(os.linesep)

    def writeBar(self, bar_):
        adjClose = bar_.getAdjClose()
        if adjClose is None:
            adjClose = ''
        dateTime = bar_.getDateTime().strftime(datetime_format)
        self.__writeLine(dateTime, bar_.getOpen(), bar_.getHigh(), bar_.getLow(), bar_.getClose(), bar_.getVolume(), adjClose)
        return

    def close(self):
        self.__file.close()


def resample_impl(barFeed, frequency, csvFile):
    instruments = barFeed.getRegisteredInstruments()
    if len(instruments) != 1:
        raise Exception('Only barfeeds with 1 instrument can be resampled')
    csvWriter = CSVFileWriter(csvFile)

    def on_bar(ds, dateTime, value):
        csvWriter.writeBar(value)

    insrumentDS = barFeed[instruments[0]]
    resampledDS = resampled.ResampledBarDataSeries(insrumentDS, frequency)
    resampledDS.getNewValueEvent().subscribe(on_bar)
    disp = dispatcher.Dispatcher()
    disp.addSubject(barFeed)
    disp.run()
    resampledDS.pushLast()


def resample_to_csv(barFeed, frequency, csvFile):
    """Resample a BarFeed into a CSV file grouping bars by a certain frequency.
    The resulting file can be loaded using :class:`pyalgotrade.barfeed.csvfeed.GenericBarFeed`.
    The CSV file will have the following format:
    ::

        Date Time,Open,High,Low,Close,Volume,Adj Close
        2013-01-01 00:00:00,13.51001,13.56,13.51,13.56,273.88014126,13.51001

    :param barFeed: The bar feed that will provide the bars. It should only hold bars from a single instrument.
    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`
    :param frequency: The grouping frequency in seconds. Must be > 0.
    :param csvFile: The path to the CSV file to write.
    :type csvFile: string.

    .. note::
        * Datetimes are stored without timezone information.
        * **Adj Close** column may be empty if the input bar feed doesn't have that info.
        * Supported resampling frequencies are:
            * Less than bar.Frequency.DAY
            * bar.Frequency.DAY
            * bar.Frequency.MONTH
    """
    assert frequency > 0, 'Invalid frequency'
    resample_impl(barFeed, frequency, csvFile)