# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\eventprofiler.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 9155 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import numpy as np
import matplotlib.pyplot as plt
from six.moves import xrange
from pyalgotrade.technical import roc
from pyalgotrade import dispatcher

class Results(object):
    __doc__ = 'Results from the profiler.'

    def __init__(self, eventsDict, lookBack, lookForward):
        assert lookBack > 0
        assert lookForward > 0
        self._Results__lookBack = lookBack
        self._Results__lookForward = lookForward
        self._Results__values = [[] for i in xrange(lookBack + lookForward + 1)]
        self._Results__eventCount = 0
        for instrument, events in eventsDict.items():
            for event in events:
                if event.isComplete():
                    self._Results__eventCount += 1
                    values = np.cumprod(event.getValues() + 1)
                    values = values / values[event.getLookBack()]
                    for t in range(event.getLookBack() * -1, event.getLookForward() + 1):
                        self.setValue(t, values[(t + event.getLookBack())])

    def __mapPos(self, t):
        if not (t >= -1 * self._Results__lookBack and t <= self._Results__lookForward):
            raise AssertionError
        return t + self._Results__lookBack

    def setValue(self, t, value):
        if value is None:
            raise Exception('Invalid value at time %d' % t)
        pos = self._Results__mapPos(t)
        self._Results__values[pos].append(value)

    def getValues(self, t):
        pos = self._Results__mapPos(t)
        return self._Results__values[pos]

    def getLookBack(self):
        return self._Results__lookBack

    def getLookForward(self):
        return self._Results__lookForward

    def getEventCount(self):
        """Returns the number of events occurred. Events that are on the boundary are skipped."""
        return self._Results__eventCount


class Predicate(object):
    __doc__ = 'Base class for event identification. You should subclass this to implement\n    the event identification logic.'

    def eventOccurred(self, instrument, bards):
        """Override (**mandatory**) to determine if an event took place in the last bar (bards[-1]).

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param bards: The BarDataSeries for the given instrument.
        :type bards: :class:`pyalgotrade.dataseries.bards.BarDataSeries`.
        :rtype: boolean.
        """
        raise NotImplementedError()


class Event(object):

    def __init__(self, lookBack, lookForward):
        assert lookBack > 0
        assert lookForward > 0
        self._Event__lookBack = lookBack
        self._Event__lookForward = lookForward
        self._Event__values = np.empty(lookBack + lookForward + 1)
        self._Event__values[:] = np.NAN

    def __mapPos(self, t):
        if not (t >= -1 * self._Event__lookBack and t <= self._Event__lookForward):
            raise AssertionError
        return t + self._Event__lookBack

    def isComplete(self):
        return not any(np.isnan(self._Event__values))

    def getLookBack(self):
        return self._Event__lookBack

    def getLookForward(self):
        return self._Event__lookForward

    def setValue(self, t, value):
        if value is not None:
            pos = self._Event__mapPos(t)
            self._Event__values[pos] = value

    def getValue(self, t):
        pos = self._Event__mapPos(t)
        return self._Event__values[pos]

    def getValues(self):
        return self._Event__values


class Profiler(object):
    __doc__ = 'This class is responsible for scanning over historical data and analyzing returns before\n    and after the events.\n\n    :param predicate: A :class:`Predicate` subclass responsible for identifying events.\n    :type predicate: :class:`Predicate`.\n    :param lookBack: The number of bars before the event to analyze. Must be > 0.\n    :type lookBack: int.\n    :param lookForward: The number of bars after the event to analyze. Must be > 0.\n    :type lookForward: int.\n    '

    def __init__(self, predicate, lookBack, lookForward):
        assert lookBack > 0
        assert lookForward > 0
        self._Profiler__predicate = predicate
        self._Profiler__lookBack = lookBack
        self._Profiler__lookForward = lookForward
        self._Profiler__feed = None
        self._Profiler__rets = {}
        self._Profiler__futureRets = {}
        self._Profiler__events = {}

    def __addPastReturns(self, instrument, event):
        begin = (event.getLookBack() + 1) * -1
        for t in xrange(begin, 0):
            try:
                ret = self._Profiler__rets[instrument][t]
                if ret is not None:
                    event.setValue(t + 1, ret)
            except IndexError:
                pass

    def __addCurrentReturns(self, instrument):
        nextTs = []
        for event, t in self._Profiler__futureRets[instrument]:
            event.setValue(t, self._Profiler__rets[instrument][(-1)])
            if t < event.getLookForward():
                t += 1
                nextTs.append((event, t))

        self._Profiler__futureRets[instrument] = nextTs

    def __onBars(self, dateTime, bars):
        for instrument in bars.getInstruments():
            self._Profiler__addCurrentReturns(instrument)
            eventOccurred = self._Profiler__predicate.eventOccurred(instrument, self._Profiler__feed[instrument])
            if eventOccurred:
                event = Event(self._Profiler__lookBack, self._Profiler__lookForward)
                self._Profiler__events[instrument].append(event)
                self._Profiler__addPastReturns(instrument, event)
                self._Profiler__futureRets[instrument].append((event, 1))

    def getResults(self):
        """Returns the results of the analysis.

        :rtype: :class:`Results`.
        """
        return Results(self._Profiler__events, self._Profiler__lookBack, self._Profiler__lookForward)

    def run(self, feed, useAdjustedCloseForReturns=True):
        """Runs the analysis using the bars supplied by the feed.

        :param barFeed: The bar feed to use to run the analysis.
        :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`.
        :param useAdjustedCloseForReturns: True if adjusted close values should be used to calculate returns.
        :type useAdjustedCloseForReturns: boolean.
        """
        if useAdjustedCloseForReturns:
            assert feed.barsHaveAdjClose(), "Feed doesn't have adjusted close values"
        try:
            self._Profiler__feed = feed
            self._Profiler__rets = {}
            self._Profiler__futureRets = {}
            for instrument in feed.getRegisteredInstruments():
                self._Profiler__events.setdefault(instrument, [])
                self._Profiler__futureRets[instrument] = []
                if useAdjustedCloseForReturns:
                    ds = feed[instrument].getAdjCloseDataSeries()
                else:
                    ds = feed[instrument].getCloseDataSeries()
                self._Profiler__rets[instrument] = roc.RateOfChange(ds, 1)

            feed.getNewValuesEvent().subscribe(self._Profiler__onBars)
            disp = dispatcher.Dispatcher()
            disp.addSubject(feed)
            disp.run()
        finally:
            feed.getNewValuesEvent().unsubscribe(self._Profiler__onBars)


def build_plot(profilerResults):
    x = []
    mean = []
    std = []
    for t in xrange(profilerResults.getLookBack() * -1, profilerResults.getLookForward() + 1):
        x.append(t)
        values = np.asarray(profilerResults.getValues(t))
        mean.append(values.mean())
        std.append(values.std())

    plt.clf()
    plt.plot(x, mean, color='#0000FF')
    lookBack = profilerResults.getLookBack()
    firstLookForward = lookBack + 1
    plt.errorbar(x=(x[firstLookForward:]),
      y=(mean[firstLookForward:]),
      yerr=(std[firstLookForward:]),
      capsize=3,
      ecolor='#AAAAFF',
      alpha=0.5)
    plt.axhline(y=(mean[lookBack]),
      xmin=(-1 * profilerResults.getLookBack()),
      xmax=(profilerResults.getLookForward()),
      color='#000000')
    plt.xlim(profilerResults.getLookBack() * -1 - 0.5, profilerResults.getLookForward() + 0.5)
    plt.xlabel('Time')
    plt.ylabel('Cumulative returns')


def plot(profilerResults):
    """Plots the result of the analysis.

    :param profilerResults: The result of the analysis
    :type profilerResults: :class:`Results`.
    """
    build_plot(profilerResults)
    plt.show()