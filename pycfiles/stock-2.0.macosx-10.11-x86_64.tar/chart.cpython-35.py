# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/service/chart.py
# Compiled at: 2017-01-15 03:23:28
# Size of source mod 2**32: 1441 bytes
import pandas as pd

def stochastic_k(prices, k):
    l = pd.rolling_min(prices, k)
    h = pd.rolling_max(prices, k)
    return 100 * (prices - l) / (h - l)


def stochastic_d(prices, k, d):
    return pd.rolling_mean(stochastic_k(prices, k), d)


def stochastic_sd(prices, k, d, sd):
    return pd.rolling_mean(stochastic_d(prices, k, d), sd)


def bollinger_band(prices, period, sigma):
    mean = pd.rolling_mean(prices, period)
    std = pd.rolling_std(prices, period)
    return mean + sigma * std


def macd_line(series, fast=26, slow=12, signal=9):
    return pd.ewma(series, span=slow) - pd.ewma(series, span=fast)


def macd_signal(series, fast=26, slow=12, signal=9):
    return pd.ewma(macd_line(series, fast=fast, slow=slow, signal=signal), span=signal)


def rsi(prices, period=14):
    diff = (prices - prices.shift(1)).fillna(0)

    def calc(p):
        gain = p[(p > 0)].sum() / period
        loss = -p[(p < 0)].sum() / period
        rs = gain / loss
        return 100 - 100 / (1 + rs)

    return pd.rolling_apply(diff, period, calc)