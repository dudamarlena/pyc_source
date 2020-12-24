# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tap_strava/sync.py
# Compiled at: 2019-06-01 00:56:54
# Size of source mod 2**32: 2251 bytes
import json
from stravalib.model import BaseEntity
import singer
import singer.metrics as metrics
from singer import metadata
from singer import Transformer
LOGGER = singer.get_logger()

def sync_stream(state, start_date, instance):
    stream = instance.stream
    if instance.replication_method == 'INCREMENTAL':
        if not state.get('bookmarks', {}).get(stream.tap_stream_id, {}).get(instance.replication_key):
            singer.write_bookmark(state, stream.tap_stream_id, instance.replication_key, start_date)
    parent_stream = stream
    with metrics.record_counter(stream.tap_stream_id) as (counter):
        for stream, record in instance.sync(state):
            if stream.tap_stream_id == parent_stream.tap_stream_id:
                counter.increment()
            rec = json.loads(json.dumps(record, cls=StravaEncoder))
            with Transformer() as (transformer):
                rec = transformer.transform(rec, stream.schema.to_dict(), metadata.to_map(stream.metadata))
            singer.write_record(stream.tap_stream_id, rec)

        if instance.replication_method == 'INCREMENTAL':
            singer.write_state(state)
        return counter.value


class StravaEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, BaseEntity):
            obj_dict = obj.to_dict()
            for k, v in list(obj_dict.items()):
                if callable(v):
                    obj_dict.pop(k)

            return obj_dict
        if isinstance(obj, ProxyList):
            return obj.copy()
        return json.JSONEncoder.default(self, obj)