# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\data\equity_indicator.py
# Compiled at: 2018-11-22 21:40:49
# Size of source mod 2**32: 610 bytes
from strategycontainer.utils.numpy_utils import float64_dtype
from .dataset import Column, DataSet

class USEquityFundamentalMetrics(DataSet):
    ev = Column(float64_dtype)
    evebit = Column(float64_dtype)
    evebitda = Column(float64_dtype)
    marketcap = Column(float64_dtype)
    pb = Column(float64_dtype)
    pe = Column(float64_dtype)
    ps = Column(float64_dtype)


class AStockIndicator(DataSet):
    freefloatmv = Column(float64_dtype)
    pe = Column(float64_dtype)
    pettm = Column(float64_dtype)
    isst = Column(float64_dtype)
    isxst = Column(float64_dtype)