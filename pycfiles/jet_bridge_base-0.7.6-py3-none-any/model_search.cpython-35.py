# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/filters/model_search.py
# Compiled at: 2020-03-04 16:40:12
# Size of source mod 2**32: 1075 bytes
import sqlalchemy
from sqlalchemy import inspect, or_, cast
from jet_bridge_base.filters.char_filter import CharFilter
from jet_bridge_base.filters.filter import EMPTY_VALUES

def get_model_search_filter(Model):
    mapper = inspect(Model)

    class ModelSearchFilter(CharFilter):

        def filter(self, qs, value):
            value = self.clean_value(value)
            if value in EMPTY_VALUES:
                return qs

            def map_column(column):
                if isinstance(column.type, (sqlalchemy.Integer, sqlalchemy.Numeric)):
                    return cast(column, sqlalchemy.String).__eq__(value)
                if isinstance(column.type, sqlalchemy.String):
                    return column.ilike('%{}%'.format(value))
                if isinstance(column.type, sqlalchemy.JSON):
                    return cast(column, sqlalchemy.String).ilike('%{}%'.format(value))

            operators = list(filter(lambda x: x is not None, map(map_column, mapper.columns)))
            return qs.filter(or_(*operators))

    return ModelSearchFilter