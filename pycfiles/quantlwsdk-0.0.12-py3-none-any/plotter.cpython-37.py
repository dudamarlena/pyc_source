# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\../gm3\indicatorModule\pyalgotrade\plotter.py
# Compiled at: 2019-06-05 03:26:10
# Size of source mod 2**32: 16045 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import collections
import matplotlib.pyplot as plt
from matplotlib import ticker
import six
from pyalgotrade import broker
from pyalgotrade import warninghelpers

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
            self._DateTimeFilter__fromDate = fromDate
            self._DateTimeFilter__toDate = toDate

        def includeDateTime(self, dateTime):
            if self._DateTimeFilter__toDate:
                if dateTime > self._DateTimeFilter__toDate:
                    return False
            if self._DateTimeFilter__fromDate:
                if dateTime < self._DateTimeFilter__fromDate:
                    return False
            return True

    dateTimeFilter = DateTimeFilter(fromDate, toDate)
    return [x for x in dateTimes if dateTimeFilter.includeDateTime(x)]


def _post_plot_fun(subPlot, mplSubplot):
    mplSubplot.legend((list(subPlot.getAllSeries().keys())), shadow=True, loc='best')
    mplSubplot.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))


class Series(object):

    def __init__(self):
        self._Series__values = {}

    def getColor(self):
        pass

    def addValue(self, dateTime, value):
        self._Series__values[dateTime] = value

    def getValue(self, dateTime):
        return self._Series__values.get(dateTime, None)

    def getValues(self):
        return self._Series__values

    def getMarker(self):
        raise NotImplementedError()

    def needColor(self):
        raise NotImplementedError()

    def plot(self, mplSubplot, dateTimes, color):
        values = []
        for dateTime in dateTimes:
            values.append(self.getValue(dateTime))

        mplSubplot.plot(dateTimes, values, color=color, marker=(self.getMarker()))


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
        self._CustomMarker__marker = 'o'

    def needColor(self):
        return True

    def setMarker(self, marker):
        self._CustomMarker__marker = marker

    def getMarker(self):
        return self._CustomMarker__marker


class LineMarker(Series):

    def __init__(self):
        super(LineMarker, self).__init__()
        self._LineMarker__marker = ' '

    def needColor(self):
        return True

    def setMarker(self, marker):
        self._LineMarker__marker = marker

    def getMarker(self):
        return self._LineMarker__marker


class InstrumentMarker(Series):

    def __init__(self):
        super(InstrumentMarker, self).__init__()
        self._InstrumentMarker__useAdjClose = None
        self._InstrumentMarker__marker = ' '

    def needColor(self):
        return True

    def setMarker(self, marker):
        self._InstrumentMarker__marker = marker

    def getMarker(self):
        return self._InstrumentMarker__marker

    def setUseAdjClose(self, useAdjClose):
        self._InstrumentMarker__useAdjClose = useAdjClose

    def getValue(self, dateTime):
        ret = Series.getValue(self, dateTime)
        if ret is not None:
            if self._InstrumentMarker__useAdjClose is None:
                ret = ret.getPrice()
            else:
                if self._InstrumentMarker__useAdjClose:
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


class MACDMarker(HistogramMarker):

    def getColorForValue(self, value, default):
        ret = default
        if value >= 0:
            ret = 'g'
        else:
            ret = 'r'
        return ret


class Subplot(object):
    __doc__ = ' '
    colors = ['b', 'c', 'm', 'y', 'k']

    def __init__(self):
        self._Subplot__series = {}
        self._Subplot__callbacks = {}
        self._Subplot__nextColor = 0

    def __getColor(self, series):
        ret = series.getColor()
        if ret is None:
            ret = Subplot.colors[(self._Subplot__nextColor % len(Subplot.colors))]
            self._Subplot__nextColor += 1
        return ret

    def isEmpty(self):
        return len(self._Subplot__series) == 0

    def getAllSeries(self):
        return self._Subplot__series

    def addDataSeries(self, label, dataSeries, defaultClass=LineMarker):
        """Add a DataSeries to the subplot.

        :param label: A name for the DataSeries values.
        :type label: string.
        :param dataSeries: The DataSeries to add.
        :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
        """
        callback = lambda bars: get_last_value(dataSeries)
        self._Subplot__callbacks[callback] = self.getSeries(label, defaultClass)

    def addCallback(self, label, callback, defaultClass=LineMarker):
        """Add a callback that will be called on each bar.

        :param label: A name for the series values.
        :type label: string.
        :param callback: A function that receives a :class:`pyalgotrade.bar.Bars` instance as a parameter and returns a number or None.
        """
        self._Subplot__callbacks[callback] = self.getSeries(label, defaultClass)

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
        for cb, series in six.iteritems(self._Subplot__callbacks):
            series.addValue(dateTime, cb(bars))

    def getSeries(self, name, defaultClass=LineMarker):
        try:
            ret = self._Subplot__series[name]
        except KeyError:
            ret = defaultClass()
            self._Subplot__series[name] = ret

        return ret

    def getCustomMarksSeries(self, name):
        return self.getSeries(name, CustomMarker)

    def plot(self, mplSubplot, dateTimes, postPlotFun=_post_plot_fun):
        for series in self._Subplot__series.values():
            color = None
            if series.needColor():
                color = self._Subplot__getColor(series)
            series.plot(mplSubplot, dateTimes, color)

        postPlotFun(self, mplSubplot)


class InstrumentSubplot(Subplot):
    __doc__ = 'A Subplot responsible for plotting an instrument.'

    def __init__(self, instrument, plotBuySell):
        super(InstrumentSubplot, self).__init__()
        self._InstrumentSubplot__instrument = instrument
        self._InstrumentSubplot__plotBuySell = plotBuySell
        self._InstrumentSubplot__instrumentSeries = self.getSeries(instrument, InstrumentMarker)

    def setUseAdjClose(self, useAdjClose):
        self._InstrumentSubplot__instrumentSeries.setUseAdjClose(useAdjClose)

    def onBars(self, bars):
        super(InstrumentSubplot, self).onBars(bars)
        bar = bars.getBar(self._InstrumentSubplot__instrument)
        if bar:
            dateTime = bars.getDateTime()
            self._InstrumentSubplot__instrumentSeries.addValue(dateTime, bar)

    def onOrderEvent(self, broker_, orderEvent):
        order = orderEvent.getOrder()
        if self._InstrumentSubplot__plotBuySell:
            if orderEvent.getEventType() in (broker.OrderEvent.Type.PARTIALLY_FILLED, broker.OrderEvent.Type.FILLED):
                if order.getInstrument() == self._InstrumentSubplot__instrument:
                    action = order.getAction()
                    execInfo = orderEvent.getEventInfo()
                    if action in [broker.Order.Action.BUY, broker.Order.Action.BUY_TO_COVER]:
                        self.getSeries('Buy', BuyMarker).addValue(execInfo.getDateTime(), execInfo.getPrice())
                    else:
                        if action in [broker.Order.Action.SELL, broker.Order.Action.SELL_SHORT]:
                            self.getSeries('Sell', SellMarker).addValue(execInfo.getDateTime(), execInfo.getPrice())


class StrategyPlotter(object):
    __doc__ = 'Class responsible for plotting a strategy execution.\n\n    :param strat: The strategy to plot.\n    :type strat: :class:`pyalgotrade.strategy.BaseStrategy`.\n    :param plotAllInstruments: Set to True to get a subplot for each instrument available.\n    :type plotAllInstruments: boolean.\n    :param plotBuySell: Set to True to get the buy/sell events plotted for each instrument available.\n    :type plotBuySell: boolean.\n    :param plotPortfolio: Set to True to get the portfolio value (shares + cash) plotted.\n    :type plotPortfolio: boolean.\n    '

    def __init__(self, strat, plotAllInstruments=True, plotBuySell=True, plotPortfolio=True):
        self._StrategyPlotter__dateTimes = set()
        self._StrategyPlotter__plotAllInstruments = plotAllInstruments
        self._StrategyPlotter__plotBuySell = plotBuySell
        self._StrategyPlotter__barSubplots = {}
        self._StrategyPlotter__namedSubplots = collections.OrderedDict()
        self._StrategyPlotter__portfolioSubplot = None
        if plotPortfolio:
            self._StrategyPlotter__portfolioSubplot = Subplot()
        strat.getBarsProcessedEvent().subscribe(self._StrategyPlotter__onBarsProcessed)
        strat.getBroker().getOrderUpdatedEvent().subscribe(self._StrategyPlotter__onOrderEvent)

    def __checkCreateInstrumentSubplot(self, instrument):
        if instrument not in self._StrategyPlotter__barSubplots:
            self.getInstrumentSubplot(instrument)

    def __onBarsProcessed(self, strat, bars):
        dateTime = bars.getDateTime()
        self._StrategyPlotter__dateTimes.add(dateTime)
        if self._StrategyPlotter__plotAllInstruments:
            for instrument in bars.getInstruments():
                self._StrategyPlotter__checkCreateInstrumentSubplot(instrument)

        for subplot in self._StrategyPlotter__namedSubplots.values():
            subplot.onBars(bars)

        for subplot in self._StrategyPlotter__barSubplots.values():
            subplot.onBars(bars)

        if self._StrategyPlotter__portfolioSubplot:
            self._StrategyPlotter__portfolioSubplot.getSeries('Portfolio').addValue(dateTime, strat.getBroker().getEquity())
            self._StrategyPlotter__portfolioSubplot.onBars(bars)

    def __onOrderEvent(self, broker_, orderEvent):
        for subplot in self._StrategyPlotter__barSubplots.values():
            subplot.onOrderEvent(broker_, orderEvent)

    def getInstrumentSubplot(self, instrument):
        """Returns the InstrumentSubplot for a given instrument

        :rtype: :class:`InstrumentSubplot`.
        """
        try:
            ret = self._StrategyPlotter__barSubplots[instrument]
        except KeyError:
            ret = InstrumentSubplot(instrument, self._StrategyPlotter__plotBuySell)
            self._StrategyPlotter__barSubplots[instrument] = ret

        return ret

    def getOrCreateSubplot(self, name):
        """Returns a Subplot by name. If the subplot doesn't exist, it gets created.

        :param name: The name of the Subplot to get or create.
        :type name: string.
        :rtype: :class:`Subplot`.
        """
        try:
            ret = self._StrategyPlotter__namedSubplots[name]
        except KeyError:
            ret = Subplot()
            self._StrategyPlotter__namedSubplots[name] = ret

        return ret

    def getPortfolioSubplot(self):
        """Returns the subplot where the portfolio values get plotted.

        :rtype: :class:`Subplot`.
        """
        return self._StrategyPlotter__portfolioSubplot

    def __buildFigureImpl(self, fromDateTime=None, toDateTime=None, postPlotFun=_post_plot_fun):
        dateTimes = _filter_datetimes(self._StrategyPlotter__dateTimes, fromDateTime, toDateTime)
        dateTimes.sort()
        subplots = []
        subplots.extend(self._StrategyPlotter__barSubplots.values())
        subplots.extend(self._StrategyPlotter__namedSubplots.values())
        if self._StrategyPlotter__portfolioSubplot is not None:
            subplots.append(self._StrategyPlotter__portfolioSubplot)
        fig, axes = plt.subplots(nrows=(len(subplots)), sharex=True, squeeze=False)
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
        """
        Build a matplotlib.figure.Figure with the subplots. Must be called after running the strategy.

        :param fromDateTime: An optional starting datetime.datetime. Everything before it won't get plotted.
        :type fromDateTime: datetime.datetime
        :param toDateTime: An optional ending datetime.datetime. Everything after it won't get plotted.
        :type toDateTime: datetime.datetime
        :rtype: A 2 element tuple with matplotlib.figure.Figure and subplots.
        """
        fig, mplSubplots = self._StrategyPlotter__buildFigureImpl(fromDateTime, toDateTime, postPlotFun=postPlotFun)
        fig.autofmt_xdate()
        return (fig, mplSubplots)

    def plot(self, fromDateTime=None, toDateTime=None, postPlotFun=_post_plot_fun):
        """
        Plot the strategy execution. Must be called after running the strategy.

        :param fromDateTime: An optional starting datetime.datetime. Everything before it won't get plotted.
        :type fromDateTime: datetime.datetime
        :param toDateTime: An optional ending datetime.datetime. Everything after it won't get plotted.
        :type toDateTime: datetime.datetime
        """
        fig, mplSubplots = self._StrategyPlotter__buildFigureImpl(fromDateTime, toDateTime, postPlotFun=postPlotFun)
        fig.autofmt_xdate()
        plt.show()

    def savePlot(self, filename, dpi=None, format='png', fromDateTime=None, toDateTime=None):
        """
        Plot the strategy execution into a file. Must be called after running the strategy.

        :param filename: The filename.
        :param dpi: The resolution in dots per inch.
        :param format: The file extension.
        :param fromDateTime: An optional starting datetime.datetime. Everything before it won't get plotted.
        :type fromDateTime: datetime.datetime
        :param toDateTime: An optional ending datetime.datetime. Everything after it won't get plotted.
        :type toDateTime: datetime.datetime
        """
        fig, mplSubplots = self._StrategyPlotter__buildFigureImpl(fromDateTime=fromDateTime, toDateTime=toDateTime)
        fig.autofmt_xdate()
        fig.savefig(filename, dpi=dpi, bbox_inches='tight', format=format)