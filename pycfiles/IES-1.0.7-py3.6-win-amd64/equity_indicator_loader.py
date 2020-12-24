# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\loaders\equity_indicator_loader.py
# Compiled at: 2018-11-13 01:48:17
# Size of source mod 2**32: 2928 bytes
from strategycontainer.lib.adjusted_array import AdjustedArray
from strategycontainer.model import Equity
from .base import PipelineLoader
from strategycontainer.utils.numpy_utils import as_column

class USEquityIndicatorLoader(PipelineLoader):

    def __init__(self, var):
        self.var = var

    def load_adjusted_array(self, columns, dates, assets, mask):
        colnames = [c.name for c in columns]
        assets = [Equity(sid, '') for sid in assets]
        singleAsset = len(assets) == 1
        singleCol = len(colnames) == 1
        price = self.var.ips_api._framework_getHistory(assets, colnames, len(dates), 'd', dates[(-1)].strftime('%Y%m%d') + self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%H%M'), False)
        raw_arrays = []
        if singleAsset:
            if singleCol:
                raw_arrays.append(as_column(price.values))
        if not singleAsset and singleCol:
            raw_arrays.append(price.values)
        elif singleAsset and not singleCol:
            for col in colnames:
                raw_arrays.append(as_column(price[col].values))

        else:
            if not singleAsset:
                if not singleCol:
                    for col in colnames:
                        raw_arrays.append(price[col].values)

        adjustments = [{} for _ in range(len(raw_arrays))]
        out = {}
        for c, c_raw, c_adjs in zip(columns, raw_arrays, adjustments):
            out[c] = AdjustedArray(c_raw.astype(c.dtype), c_adjs, c.missing_value)

        return out


class AStockIndicatorLoader(PipelineLoader):

    def __init__(self, var):
        self.var = var

    def load_adjusted_array(self, columns, dates, assets, mask):
        colnames = [c.name for c in columns]
        assets = [Equity(sid, '') for sid in assets]
        singleAsset = len(assets) == 1
        singleCol = len(colnames) == 1
        price = self.var.ips_api._framework_getHistory(assets, colnames, len(dates), 'd', dates[(-1)].strftime('%Y%m%d') + self.var._FRAMEWORK_BT_CURRENTTIME.strftime('%H%M'), False)
        raw_arrays = []
        if singleAsset:
            if singleCol:
                raw_arrays.append(as_column(price.values))
        if not singleAsset and singleCol:
            raw_arrays.append(price.values)
        elif singleAsset and not singleCol:
            for col in colnames:
                raw_arrays.append(as_column(price[col].values))

        else:
            if not singleAsset:
                if not singleCol:
                    for col in colnames:
                        raw_arrays.append(price[col].values)

        adjustments = [{} for _ in range(len(raw_arrays))]
        out = {}
        for c, c_raw, c_adjs in zip(columns, raw_arrays, adjustments):
            out[c] = AdjustedArray(c_raw.astype(c.dtype), c_adjs, c.missing_value)

        return out