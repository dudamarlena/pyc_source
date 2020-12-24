# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/filters/model_aggregate.py
# Compiled at: 2019-09-29 04:07:46
from sqlalchemy import func, sql
from jet_bridge_base.filters.char_filter import CharFilter
from jet_bridge_base.filters.filter import EMPTY_VALUES

class ModelAggregateFilter(CharFilter):

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        y_column = getattr(self.model, value['y_column'])
        if value['y_func'] == 'count':
            y_func = func.count(y_column)
        elif value['y_func'] == 'sum':
            y_func = func.sum(y_column)
        elif value['y_func'] == 'min':
            y_func = func.min(y_column)
        elif value['y_func'] == 'max':
            y_func = func.max(y_column)
        elif value['y_func'] == 'avg':
            y_func = func.avg(y_column)
        else:
            return qs.filter(sql.false())
        qs = qs.session.query(y_func).one()
        return qs