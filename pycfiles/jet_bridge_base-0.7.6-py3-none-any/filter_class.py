# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/filters/filter_class.py
# Compiled at: 2019-10-06 09:38:40
from sqlalchemy import inspect
from jet_bridge_base.filters import lookups
from jet_bridge_base.filters.filter import Filter
from jet_bridge_base.filters.filter_for_dbfield import filter_for_data_type

class FilterClass(object):
    filters = []

    def __init__(self, *args, **kwargs):
        self.meta = getattr(self, 'Meta', None)
        if 'context' in kwargs:
            self.request = kwargs['context'].get('request', None)
            self.handler = kwargs['context'].get('handler', None)
        self.update_filters()
        return

    def update_filters(self):
        filters = []
        if self.meta:
            if hasattr(self.meta, 'model'):
                Model = self.meta.model
                mapper = inspect(Model)
                columns = mapper.columns
                if hasattr(self.meta, 'fields'):
                    columns = filter(lambda x: x.name in self.meta.fields, columns)
                for column in columns:
                    item = filter_for_data_type(column.type)
                    for lookup in item['lookups']:
                        instance = item['filter_class'](field_name=column.key, model=Model, lookup=lookup, request=self.request, handler=self.handler)
                        filters.append(instance)

        declared_filters = filter(lambda x: isinstance(x[1], Filter), map(lambda x: (x, getattr(self, x)), dir(self)))
        for filter_name, filter_item in declared_filters:
            filter_item.name = filter_name
            filter_item.model = Model
            filter_item.request = self.request
            filter_item.handler = self.handler
            filters.append(filter_item)

        self.filters = filters

    def filter_queryset(self, queryset):
        for item in self.filters:
            if self.handler and item.name:
                argument_name = ('{}__{}').format(item.name, item.lookup)
                value = self.handler.request.get_argument(argument_name, None)
                if value is None and item.lookup == lookups.DEFAULT_LOOKUP:
                    value = self.handler.request.get_argument(item.name, None)
            else:
                value = None
            queryset = item.filter(queryset, value)

        return queryset