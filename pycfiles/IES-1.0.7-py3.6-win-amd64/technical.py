# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\factors\technical.py
# Compiled at: 2018-01-16 04:50:03
# Size of source mod 2**32: 12085 bytes
"""
Technical Analysis Factors
--------------------------
"""
from __future__ import division
from numpy import abs, average, clip, diff, dstack, inf
from numexpr import evaluate
from strategycontainer.tsp.data import USEquityPricing
from strategycontainer.tsp.factors import CustomFactor
from strategycontainer.tsp.mixins import SingleInputMixin
from strategycontainer.utils.input_validation import expect_bounded
from strategycontainer.utils.math_utils import nanargmax, nanargmin, nanmax, nanmean, nanstd, nanmin
from strategycontainer.utils.numpy_utils import rolling_window
from .basic import exponential_weights
from .basic import LinearWeightedMovingAverage, MaxDrawdown, SimpleMovingAverage, VWAP, WeightedAverageValue

class RSI(CustomFactor, SingleInputMixin):
    __doc__ = '\n    Relative Strength Index\n\n    **Default Inputs**: [USEquityPricing.close]\n\n    **Default Window Length**: 15\n    '
    window_length = 15
    inputs = (USEquityPricing.close,)
    window_safe = True

    def compute(self, today, assets, out, closes):
        diffs = diff(closes, axis=0)
        ups = nanmean((clip(diffs, 0, inf)), axis=0)
        downs = abs(nanmean((clip(diffs, -inf, 0)), axis=0))
        return evaluate('100 - (100 / (1 + (ups / downs)))',
          local_dict={'ups':ups, 
         'downs':downs},
          global_dict={},
          out=out)


class BollingerBands(CustomFactor):
    __doc__ = '\n    Bollinger Bands technical indicator.\n    https://en.wikipedia.org/wiki/Bollinger_Bands\n\n    **Default Inputs:** :data:`zipline.pipeline.data.USEquityPricing.close`\n\n    Parameters\n    ----------\n    inputs : length-1 iterable[BoundColumn]\n        The expression over which to compute bollinger bands.\n    window_length : int > 0\n        Length of the lookback window over which to compute the bollinger\n        bands.\n    k : float\n        The number of standard deviations to add or subtract to create the\n        upper and lower bands.\n    '
    params = ('k', )
    inputs = (USEquityPricing.close,)
    outputs = ('lower', 'middle', 'upper')

    def compute(self, today, assets, out, close, k):
        difference = k * nanstd(close, axis=0)
        out.middle = middle = nanmean(close, axis=0)
        out.upper = middle + difference
        out.lower = middle - difference


class Aroon(CustomFactor):
    __doc__ = '\n    Aroon technical indicator.\n    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/aroon-indicator  # noqa\n\n    **Defaults Inputs:** USEquityPricing.low, USEquityPricing.high\n\n    Parameters\n    ----------\n    window_length : int > 0\n        Length of the lookback window over which to compute the Aroon\n        indicator.\n    '
    inputs = (
     USEquityPricing.low, USEquityPricing.high)
    outputs = ('down', 'up')

    def compute(self, today, assets, out, lows, highs):
        wl = self.window_length
        high_date_index = nanargmax(highs, axis=0)
        low_date_index = nanargmin(lows, axis=0)
        evaluate('(100 * high_date_index) / (wl - 1)',
          local_dict={'high_date_index':high_date_index, 
         'wl':wl},
          out=(out.up))
        evaluate('(100 * low_date_index) / (wl - 1)',
          local_dict={'low_date_index':low_date_index, 
         'wl':wl},
          out=(out.down))


class FastStochasticOscillator(CustomFactor):
    __doc__ = '\n    Fast Stochastic Oscillator Indicator [%K, Momentum Indicator]\n    https://wiki.timetotrade.eu/Stochastic\n\n    This stochastic is considered volatile, and varies a lot when used in\n    market analysis. It is recommended to use the slow stochastic oscillator\n    or a moving average of the %K [%D].\n\n    **Default Inputs:** :data: `zipline.pipeline.data.USEquityPricing.close`\n                        :data: `zipline.pipeline.data.USEquityPricing.low`\n                        :data: `zipline.pipeline.data.USEquityPricing.high`\n\n    **Default Window Length:** 14\n\n    Returns\n    -------\n    out: %K oscillator\n    '
    inputs = (USEquityPricing.close, USEquityPricing.low, USEquityPricing.high)
    window_safe = True
    window_length = 14

    def compute(self, today, assets, out, closes, lows, highs):
        highest_highs = nanmax(highs, axis=0)
        lowest_lows = nanmin(lows, axis=0)
        today_closes = closes[(-1)]
        evaluate('((tc - ll) / (hh - ll)) * 100',
          local_dict={'tc':today_closes, 
         'll':lowest_lows, 
         'hh':highest_highs},
          global_dict={},
          out=out)


class IchimokuKinkoHyo(CustomFactor):
    __doc__ = 'Compute the various metrics for the Ichimoku Kinko Hyo (Ichimoku Cloud).\n    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ichimoku_cloud  # noqa\n\n    **Default Inputs:** :data:`zipline.pipeline.data.USEquityPricing.high`\n                        :data:`zipline.pipeline.data.USEquityPricing.low`\n                        :data:`zipline.pipeline.data.USEquityPricing.close`\n    **Default Window Length:** 52\n\n    Parameters\n    ----------\n    window_length : int > 0\n        The length the the window for the senkou span b.\n    tenkan_sen_length : int >= 0, <= window_length\n        The length of the window for the tenkan-sen.\n    kijun_sen_length : int >= 0, <= window_length\n        The length of the window for the kijou-sen.\n    chikou_span_length : int >= 0, <= window_length\n        The lag for the chikou span.\n    '
    params = {'tenkan_sen_length':9, 
     'kijun_sen_length':26, 
     'chikou_span_length':26}
    inputs = (
     USEquityPricing.high, USEquityPricing.low, USEquityPricing.close)
    outputs = ('tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b', 'chikou_span')
    window_length = 52

    def _validate(self):
        super(IchimokuKinkoHyo, self)._validate()
        for k, v in self.params.items():
            if v > self.window_length:
                raise ValueError('%s must be <= the window_length: %s > %s' % (
                 k, v, self.window_length))

    def compute(self, today, assets, out, high, low, close, tenkan_sen_length, kijun_sen_length, chikou_span_length):
        out.tenkan_sen = tenkan_sen = (high[-tenkan_sen_length:].max(axis=0) + low[-tenkan_sen_length:].min(axis=0)) / 2
        out.kijun_sen = kijun_sen = (high[-kijun_sen_length:].max(axis=0) + low[-kijun_sen_length:].min(axis=0)) / 2
        out.senkou_span_a = (tenkan_sen + kijun_sen) / 2
        out.senkou_span_b = (high.max(axis=0) + low.min(axis=0)) / 2
        out.chikou_span = close[chikou_span_length]


class RateOfChangePercentage(CustomFactor):
    __doc__ = '\n    Rate of change Percentage\n    ROC measures the percentage change in price from one period to the next.\n    The ROC calculation compares the current price with the price `n`\n    periods ago.\n    Formula for calculation: ((price - prevPrice) / prevPrice) * 100\n    price - the current price\n    prevPrice - the price n days ago, equals window length\n    '

    def compute(self, today, assets, out, close):
        today_close = close[(-1)]
        prev_close = close[0]
        evaluate('((tc - pc) / pc) * 100', local_dict={'tc':today_close, 
         'pc':prev_close},
          global_dict={},
          out=out)


class TrueRange(CustomFactor):
    __doc__ = '\n    True Range\n\n    A technical indicator originally developed by J. Welles Wilder, Jr.\n    Indicates the true degree of daily price change in an underlying.\n\n    **Default Inputs:** :data:`zipline.pipeline.data.USEquityPricing.high`\n                        :data:`zipline.pipeline.data.USEquityPricing.low`\n                        :data:`zipline.pipeline.data.USEquityPricing.close`\n    **Default Window Length:** 2\n    '
    inputs = (
     USEquityPricing.high,
     USEquityPricing.low,
     USEquityPricing.close)
    window_length = 2

    def compute(self, today, assets, out, highs, lows, closes):
        high_to_low = highs[1:] - lows[1:]
        high_to_prev_close = abs(highs[1:] - closes[:-1])
        low_to_prev_close = abs(lows[1:] - closes[:-1])
        out[:] = nanmax(dstack((
         high_to_low,
         high_to_prev_close,
         low_to_prev_close)), 2)


class MovingAverageConvergenceDivergenceSignal(CustomFactor):
    __doc__ = '\n    Moving Average Convergence/Divergence (MACD) Signal line\n    https://en.wikipedia.org/wiki/MACD\n\n    A technical indicator originally developed by Gerald Appel in the late\n    1970\'s. MACD shows the relationship between two moving averages and\n    reveals changes in the strength, direction, momentum, and duration of a\n    trend in a stock\'s price.\n\n    **Default Inputs:** :data:`zipline.pipeline.data.USEquityPricing.close`\n\n    Parameters\n    ----------\n    fast_period : int > 0, optional\n        The window length for the "fast" EWMA. Default is 12.\n    slow_period : int > 0, > fast_period, optional\n        The window length for the "slow" EWMA. Default is 26.\n    signal_period : int > 0, < fast_period, optional\n        The window length for the signal line. Default is 9.\n\n    Notes\n    -----\n    Unlike most pipeline expressions, this factor does not accept a\n    ``window_length`` parameter. ``window_length`` is inferred from\n    ``slow_period`` and ``signal_period``.\n    '
    inputs = (USEquityPricing.close,)
    params = ('fast_period', 'slow_period', 'signal_period')

    @expect_bounded(__funcname='MACDSignal',
      fast_period=(1, None),
      slow_period=(1, None),
      signal_period=(1, None))
    def __new__(cls, fast_period=12, slow_period=26, signal_period=9, *args, **kwargs):
        if slow_period <= fast_period:
            raise ValueError("'slow_period' must be greater than 'fast_period', but got\nslow_period={slow}, fast_period={fast}".format(slow=slow_period,
              fast=fast_period))
        return (super(MovingAverageConvergenceDivergenceSignal, cls).__new__)(
 cls, *args, fast_period=fast_period, slow_period=slow_period, signal_period=signal_period, window_length=slow_period + signal_period - 1, **kwargs)

    def _ewma(self, data, length):
        decay_rate = 1.0 - 2.0 / (1.0 + length)
        return average(data,
          axis=1,
          weights=(exponential_weights(length, decay_rate)))

    def compute(self, today, assets, out, close, fast_period, slow_period, signal_period):
        slow_EWMA = self._ewma(rolling_window(close, slow_period), slow_period)
        fast_EWMA = self._ewma(rolling_window(close, fast_period)[-signal_period:], fast_period)
        macd = fast_EWMA - slow_EWMA
        out[:] = self._ewma(macd.T, signal_period)


MACDSignal = MovingAverageConvergenceDivergenceSignal