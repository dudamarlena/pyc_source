# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/plotter.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import collections, broker
from pyalgotrade import warninghelpers
import matplotlib.pyplot as plt
from matplotlib import ticker

def get_last_value(dataSeries):
    ret = None
    try:
        ret = dataSeries[(-1)]
    except IndexError:
        pass

    return ret


def _filter_datetimes(dateTimes, fromDate=None, toDate=None):

    class DateTimeFilter(object):

        def __init__(self, fromDate=None, toDate=None):
            self.__fromDate = fromDate
            self.__toDate = toDate

        def includeDateTime(self, dateTime):
            if self.__toDate and dateTime > self.__toDate:
                return False
            if self.__fromDate and dateTime < self.__fromDate:
                return False
            return True

    dateTimeFilter = DateTimeFilter(fromDate, toDate)
    return filter(lambda x: dateTimeFilter.includeDateTime(x), dateTimes)


def _post_plot_fun(subPlot, mplSubplot):
    mplSubplot.legend(subPlot.getAllSeries().keys(), shadow=True, loc='best')
    mplSubplot.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))


class Series(object):

    def __init__(self):
        self.__values = {}

    def getColor(self):
        return

    def addValue(self, dateTime, value):
        self.__values[dateTime] = value

    def getValue(self, dateTime):
        return self.__values.get(dateTime, None)

    def getValues(self):
        return self.__values

    def getMarker(self):
        raise NotImplementedError()

    def needColor(self):
        raise NotImplementedError()

    def plot(self, mplSubplot, dateTimes, color):
        values = []
        for dateTime in dateTimes:
            values.append(self.getValue(dateTime))

        mplSubplot.plot(dateTimes, values, color=color, marker=self.getMarker())


class BuyMarker(Series):

    def getColor(self):
        return 'g'

    def getMarker(self):
        return '^'

    def needColor(self):
        return True


class SellMarker(Series):

    def getColor(self):
        return 'r'

    def getMarker(self):
        return 'v'

    def needColor(self):
        return True


class CustomMarker(Series):

    def __init__(self):
        super(CustomMarker, self).__init__()
        self.__marker = 'o'

    def needColor(self):
        return True

    def setMarker(self, marker):
        self.__marker = marker

    def getMarker(self):
        return self.__marker


class LineMarker(Series):

    def __init__(self):
        super(LineMarker, self).__init__()
        self.__marker = ' '

    def needColor(self):
        return True

    def setMarker(self, marker):
        self.__marker = marker

    def getMarker(self):
        return self.__marker


class InstrumentMarker(Series):

    def __init__(self):
        super(InstrumentMarker, self).__init__()
        self.__useAdjClose = None
        self.__marker = ' '
        return

    def needColor(self):
        return True

    def setMarker(self, marker):
        self.__marker = marker

    def getMarker(self):
        return self.__marker

    def setUseAdjClose(self, useAdjClose):
        self.__useAdjClose = useAdjClose

    def getValue(self, dateTime):
        ret = Series.getValue(self, dateTime)
        if ret is not None:
            if self.__useAdjClose is None:
                ret = ret.getPrice()
            elif self.__useAdjClose:
                ret = ret.getAdjClose()
            else:
                ret = ret.getClose()
        return ret


class HistogramMarker(Series):

    def needColor(self):
        return True

    def getColorForValue(self, value, default):
        return default

    def plot(self, mplSubplot, dateTimes, color):
        validDateTimes = []
        values = []
        colors = []
        for dateTime in dateTimes:
            value = self.getValue(dateTime)
            if value is not None:
                validDateTimes.append(dateTime)
                values.append(value)
                colors.append(self.getColorForValue(value, color))

        mplSubplot.bar(validDateTimes, values, color=colors)
        return


class MACDMarker(HistogramMarker):

    def getColorForValue(self, value, default):
        ret = default
        if value >= 0:
            ret = 'g'
        else:
            ret = 'r'
        return ret


class Subplot(object):
    """ """
    colors = [
     'b', 'c', 'm', 'y', 'k']

    def __init__(self):
        self.__series = {}
        self.__callbacks = {}
        self.__nextColor = 0

    def __getColor(self, series):
        ret = series.getColor()
        if ret is None:
            ret = Subplot.colors[(self.__nextColor % len(Subplot.colors))]
            self.__nextColor += 1
        return ret

    def isEmpty(self):
        return len(self.__series) == 0

    def getAllSeries(self):
        return self.__series

    def addDataSeries(self, label, dataSeries, defaultClass=LineMarker):
        """Add a DataSeries to the subplot.

        :param label: A name for the DataSeries values.
        :type label: string.
        :param dataSeries: The DataSeries to add.
        :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
        """
        callback = lambda bars: get_last_value(dataSeries)
        self.__callbacks[callback] = self.getSeries(label, defaultClass)

    def addCallback(self, label, callback, defaultClass=LineMarker):
        """Add a callback that will be called on each bar.

        :param label: A name for the series values.
        :type label: string.
        :param callback: A function that receives a :class:`pyalgotrade.bar.Bars` instance as a parameter and returns a number or None.
        """
        self.__callbacks[callback] = self.getSeries(label, defaultClass)

    def addLine(self, label, level):
        """Add a horizontal line to the plot.

        :param label: A label.
        :type label: string.
        :param level: The position for the line.
        :type level: int/float.
        """
        self.addCallback(label, lambda x: level)

    def onBars(self, bars):
        dateTime = bars.getDateTime()
        for cb, series in self.__callbacks.iteritems():
            series.addValue(dateTime, cb(bars))

    def getSeries(self, name, defaultClass=LineMarker):
        try:
            ret = self.__series[name]
        except KeyError:
            ret = defaultClass()
            self.__series[name] = ret

        return ret

    def getCustomMarksSeries(self, name):
        return self.getSeries(name, CustomMarker)

    def plot(self, mplSubplot, dateTimes, postPlotFun=_post_plot_fun):
        for series in self.__series.values():
            color = None
            if series.needColor():
                color = self.__getColor(series)
            series.plot(mplSubplot, dateTimes, color)

        postPlotFun(self, mplSubplot)
        return


class InstrumentSubplot(Subplot):
    """A Subplot responsible for plotting an instrument."""

    def __init__(self, instrument, plotBuySell):
        super(InstrumentSubplot, self).__init__()
        self.__instrument = instrument
        self.__plotBuySell = plotBuySell
        self.__instrumentSeries = self.getSeries(instrument, InstrumentMarker)

    def setUseAdjClose(self, useAdjClose):
        self.__instrumentSeries.setUseAdjClose(useAdjClose)

    def onBars(self, bars):
        super(InstrumentSubplot, self).onBars(bars)
        bar = bars.getBar(self.__instrument)
        if bar:
            dateTime = bars.getDateTime()
            self.__instrumentSeries.addValue(dateTime, bar)

    def onOrderEvent(self, broker_, orderEvent):
        order = orderEvent.getOrder()
        if self.__plotBuySell and orderEvent.getEventType() in (broker.OrderEvent.Type.PARTIALLY_FILLED, broker.OrderEvent.Type.FILLED) and order.getInstrument() == self.__instrument:
            action = order.getAction()
            execInfo = orderEvent.getEventInfo()
            if action in [broker.Order.Action.BUY, broker.Order.Action.BUY_TO_COVER]:
                self.getSeries('Buy', BuyMarker).addValue(execInfo.getDateTime(), execInfo.getPrice())
            elif action in [broker.Order.Action.SELL, broker.Order.Action.SELL_SHORT]:
                self.getSeries('Sell', SellMarker).addValue(execInfo.getDateTime(), execInfo.getPrice())


class StrategyPlotter(object):
    """Class responsible for plotting a strategy execution.

    :param strat: The strategy to plot.
    :type strat: :class:`pyalgotrade.strategy.BaseStrategy`.
    :param plotAllInstruments: Set to True to get a subplot for each instrument available.
    :type plotAllInstruments: boolean.
    :param plotBuySell: Set to True to get the buy/sell events plotted for each instrument available.
    :type plotBuySell: boolean.
    :param plotPortfolio: Set to True to get the portfolio value (shares + cash) plotted.
    :type plotPortfolio: boolean.
    """

    def __init__(self, strat, plotAllInstruments=True, plotBuySell=True, plotPortfolio=True):
        self.__dateTimes = set()
        self.__plotAllInstruments = plotAllInstruments
        self.__plotBuySell = plotBuySell
        self.__barSubplots = {}
        self.__namedSubplots = collections.OrderedDict()
        self.__portfolioSubplot = None
        if plotPortfolio:
            self.__portfolioSubplot = Subplot()
        strat.getBarsProcessedEvent().subscribe(self.__onBarsProcessed)
        strat.getBroker().getOrderUpdatedEvent().subscribe(self.__onOrderEvent)
        return

    def __checkCreateInstrumentSubplot(self, instrument):
        if instrument not in self.__barSubplots:
            self.getInstrumentSubplot(instrument)

    def __onBarsProcessed(self, strat, bars):
        dateTime = bars.getDateTime()
        self.__dateTimes.add(dateTime)
        if self.__plotAllInstruments:
            for instrument in bars.getInstruments():
                self.__checkCreateInstrumentSubplot(instrument)

        for subplot in self.__namedSubplots.values():
            subplot.onBars(bars)

        for subplot in self.__barSubplots.values():
            subplot.onBars(bars)

        if self.__portfolioSubplot:
            self.__portfolioSubplot.getSeries('Portfolio').addValue(dateTime, strat.getBroker().getEquity())
            self.__portfolioSubplot.onBars(bars)

    def __onOrderEvent(self, broker_, orderEvent):
        for subplot in self.__barSubplots.values():
            subplot.onOrderEvent(broker_, orderEvent)

    def getInstrumentSubplot(self, instrument):
        """Returns the InstrumentSubplot for a given instrument

        :rtype: :class:`InstrumentSubplot`.
        """
        try:
            ret = self.__barSubplots[instrument]
        except KeyError:
            ret = InstrumentSubplot(instrument, self.__plotBuySell)
            self.__barSubplots[instrument] = ret

        return ret

    def getOrCreateSubplot(self, name):
        """Returns a Subplot by name. If the subplot doesn't exist, it gets created.

        :param name: The name of the Subplot to get or create.
        :type name: string.
        :rtype: :class:`Subplot`.
        """
        try:
            ret = self.__namedSubplots[name]
        except KeyError:
            ret = Subplot()
            self.__namedSubplots[name] = ret

        return ret

    def getPortfolioSubplot(self):
        """Returns the subplot where the portfolio values get plotted.

        :rtype: :class:`Subplot`.
        """
        return self.__portfolioSubplot

    def __buildFigureImpl(self, fromDateTime=None, toDateTime=None, postPlotFun=_post_plot_fun):
        dateTimes = _filter_datetimes(self.__dateTimes, fromDateTime, toDateTime)
        dateTimes.sort()
        subplots = []
        subplots.extend(self.__barSubplots.values())
        subplots.extend(self.__namedSubplots.values())
        if self.__portfolioSubplot is not None:
            subplots.append(self.__portfolioSubplot)
        fig, axes = plt.subplots(nrows=len(subplots), sharex=True, squeeze=False)
        mplSubplots = []
        for i, subplot in enumerate(subplots):
            axesSubplot = axes[i][0]
            if not subplot.isEmpty():
                mplSubplots.append(axesSubplot)
                subplot.plot(axesSubplot, dateTimes, postPlotFun=postPlotFun)
                axesSubplot.grid(True)

        return (
         fig, mplSubplots)

    def buildFigure(self, fromDateTime=None, toDateTime=None):
        warninghelpers.deprecation_warning('buildFigure will be deprecated in the next version. Use buildFigureAndSubplots.', stacklevel=2)
        fig, _ = self.buildFigureAndSubplots(fromDateTime, toDateTime)
        return fig

    def buildFigureAndSubplots(self, fromDateTime=None, toDateTime=None, postPlotFun=_post_plot_fun):
        """Builds a matplotlib.figure.Figure with the subplots. Must be called after running the strategy.

        :param fromDateTime: An optional starting datetime.datetime. Everything before it won't get plotted.
        :type fromDateTime: datetime.datetime
        :param toDateTime: An optional ending datetime.datetime. Everything after it won't get plotted.
        :type toDateTime: datetime.datetime
        :rtype: A 2 element tuple with matplotlib.figure.Figure and subplots.
        """
        fig, mplSubplots = self.__buildFigureImpl(fromDateTime, toDateTime, postPlotFun=postPlotFun)
        fig.autofmt_xdate()
        return (fig, mplSubplots)

    def plot(self, fromDateTime=None, toDateTime=None, postPlotFun=_post_plot_fun):
        """Plots the strategy execution. Must be called after running the strategy.

        :param fromDateTime: An optional starting datetime.datetime. Everything before it won't get plotted.
        :type fromDateTime: datetime.datetime
        :param toDateTime: An optional ending datetime.datetime. Everything after it won't get plotted.
        :type toDateTime: datetime.datetime
        """
        fig, mplSubplots = self.__buildFigureImpl(fromDateTime, toDateTime, postPlotFun=postPlotFun)
        fig.autofmt_xdate()
        plt.show()