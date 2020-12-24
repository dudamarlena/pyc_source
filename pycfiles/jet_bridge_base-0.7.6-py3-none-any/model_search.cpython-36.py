# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/filters/model_search.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 990 bytes
import sqlalchemy
from sqlalchemy import inspect, or_, cast
from jet_bridge_base.filters.char_filter import CharFilter
from jet_bridge_base.filters.filter import EMPTY_VALUES

def filter_search_field(field):
    allowed_fields = [
     sqlalchemy.String,
     sqlalchemy.JSON]
    return isinstance(field.type, tuple(allowed_fields))


def get_model_search_filter(Model):
    mapper = inspect(Model)
    search_fields = list(map(lambda x: x, filter(filter_search_field, mapper.columns)))
    primary_key_field = mapper.primary_key[0]

    class ModelSearchFilter(CharFilter):

        def filter(self, qs, value):
            value = self.clean_value(value)
            if value in EMPTY_VALUES:
                return qs
            else:
                operators = list(map(lambda x: x.ilike('%{}%'.format(value)), search_fields))
                operators.append(cast(primary_key_field, sqlalchemy.String).__eq__(value))
                return qs.filter(or_(*operators))

    return ModelSearchFilter