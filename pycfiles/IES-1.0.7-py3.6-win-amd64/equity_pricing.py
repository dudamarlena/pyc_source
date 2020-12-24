# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\data\equity_pricing.py
# Compiled at: 2018-11-13 01:42:07
# Size of source mod 2**32: 1934 bytes
"""
Dataset representing OHLCV data.
"""
from strategycontainer.utils.numpy_utils import float64_dtype
from .dataset import Column, DataSet

class USEquityPricing(DataSet):
    __doc__ = '\n    Dataset representing daily trading prices and volumes.\n    '
    open = Column(float64_dtype)
    high = Column(float64_dtype)
    low = Column(float64_dtype)
    close = Column(float64_dtype)
    volume = Column(float64_dtype)
    adj_close = Column(float64_dtype)


class AStockPricing(DataSet):
    open = Column(float64_dtype)
    high = Column(float64_dtype)
    low = Column(float64_dtype)
    close = Column(float64_dtype)
    volume = Column(float64_dtype)
    amount = Column(float64_dtype)
    pre_open = Column(float64_dtype)
    pre_high = Column(float64_dtype)
    pre_low = Column(float64_dtype)
    pre_close = Column(float64_dtype)
    pre_volume = Column(float64_dtype)
    post_open = Column(float64_dtype)
    post_high = Column(float64_dtype)
    post_low = Column(float64_dtype)
    post_close = Column(float64_dtype)
    post_volume = Column(float64_dtype)
    tradestatus = Column(float64_dtype)
    fund_open = Column(float64_dtype)
    fund_high = Column(float64_dtype)
    fund_low = Column(float64_dtype)
    fund_close = Column(float64_dtype)
    fund_volume = Column(float64_dtype)
    pre_fund_open = Column(float64_dtype)
    pre_fund_high = Column(float64_dtype)
    pre_fund_low = Column(float64_dtype)
    pre_fund_close = Column(float64_dtype)
    pre_fund_volume = Column(float64_dtype)
    fund_avgprice = Column(float64_dtype)
    fund_differ = Column(float64_dtype)
    fund_differrange = Column(float64_dtype)
    fund_turn = Column(float64_dtype)
    fund_amount = Column(float64_dtype)
    fund_amplitude = Column(float64_dtype)
    fund_discount = Column(float64_dtype)
    fund_discountrate = Column(float64_dtype)