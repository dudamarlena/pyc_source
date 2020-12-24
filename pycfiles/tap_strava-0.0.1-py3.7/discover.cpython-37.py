# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tap_strava/discover.py
# Compiled at: 2019-06-01 00:56:54
# Size of source mod 2**32: 1032 bytes
import os, json, singer
from tap_strava.streams import STREAMS

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_shared_schema_refs():
    ref_sub_path = 'shared'
    shared_schemas_path = get_abs_path('schemas/' + ref_sub_path)
    shared_file_names = [f for f in os.listdir(shared_schemas_path) if os.path.isfile(os.path.join(shared_schemas_path, f))]
    shared_schema_refs = {}
    for shared_file in shared_file_names:
        with open(os.path.join(shared_schemas_path, shared_file)) as (data_file):
            shared_schema_refs[ref_sub_path + '/' + shared_file] = json.load(data_file)

    return shared_schema_refs


def discover_streams(client):
    streams = []
    for s in STREAMS.values():
        s = s(client)
        schema = s.load_schema()
        streams.append({'stream':s.name,  'tap_stream_id':s.name,  'schema':schema,  'metadata':s.load_metadata()})

    return streams