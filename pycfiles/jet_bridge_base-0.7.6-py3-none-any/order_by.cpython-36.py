# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/filters/order_by.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 792 bytes
from sqlalchemy import sql, desc
from jet_bridge_base.filters.char_filter import CharFilter
from jet_bridge_base.filters.filter import EMPTY_VALUES

class OrderFilter(CharFilter):

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        else:
            if len(value) < 2:
                return qs.filter(sql.false())
            ordering = value.split(',')

            def map_field(name):
                descending = False
                if name.startswith('-'):
                    name = name[1:]
                    descending = True
                field = getattr(self.model, name)
                if descending:
                    field = desc(field)
                return field

            if len(ordering):
                qs = (qs.order_by)(*map(lambda x: map_field(x), ordering))
            return qs