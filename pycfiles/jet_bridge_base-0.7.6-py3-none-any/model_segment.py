# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/filters/model_segment.py
# Compiled at: 2019-09-29 04:07:46
from sqlalchemy import inspect, sql
from jet_bridge_base.filters.char_filter import CharFilter
from jet_bridge_base.filters.filter import EMPTY_VALUES
from jet_bridge_base.serializers.sql import SqlSerializer

def get_model_segment_filter(Model):
    mapper = inspect(Model)
    primary_key = mapper.primary_key[0].name

    class ModelSegmentFilter(CharFilter):

        def filter(self, qs, value):
            value = self.clean_value(value)
            if value in EMPTY_VALUES:
                return qs
            body = self.handler.data
            if not isinstance(body, dict):
                return qs.filter(sql.false())
            items = list(filter(lambda x: x.get('name') == value, body.get('segments', [])))
            if len(items) == 0:
                return qs.filter(sql.false())
            query = items[0].get('query')
            serializer = SqlSerializer(data={'query': query})
            serializer.is_valid(raise_exception=True)
            result = serializer.execute()
            columns = list(result['columns'])
            rows = result['data']
            if len(columns) == 0 or len(rows) == 0:
                return qs.filter(sql.false())
            ids = list(map(lambda x: list(x)[0], rows))
            return qs.filter(getattr(Model, primary_key).in_(ids))

    return ModelSegmentFilter