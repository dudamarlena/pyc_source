# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/filters/model_relation.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 1516 bytes
import sqlalchemy
from jet_bridge_base.filters.filter import EMPTY_VALUES
from sqlalchemy import inspect
from jet_bridge_base.db import MappedBase
from jet_bridge_base.filters.char_filter import CharFilter

def filter_search_field(field):
    allowed_fields = [
     sqlalchemy.String,
     sqlalchemy.JSON]
    return isinstance(field.type, tuple(allowed_fields))


def get_model_relation_filter(Model):
    mapper = inspect(Model)

    class ModelRelationFilter(CharFilter):

        def filter(self, qs, value):
            if value in EMPTY_VALUES:
                return qs
            else:
                current_table = mapper.tables[0]
                path = list(map(lambda x: x.split('.'), value.split('|')))
                path_len = len(path)
                for i in range(path_len):
                    item = path[i]
                    last = i == path_len - 1
                    if not last:
                        current_table_column = current_table.columns[item[0]]
                        related_table = MappedBase.metadata.tables[item[1]]
                        related_table_column = related_table.columns[item[2]]
                        qs = qs.join(related_table, current_table_column == related_table_column)
                        current_table = related_table
                    else:
                        current_table_column = current_table.columns[item[0]]
                        value = item[1].split(',')
                        qs = qs.filter(current_table_column.in_(value))

                return qs

    return ModelRelationFilter