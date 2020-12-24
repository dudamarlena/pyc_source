# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cmusselle/Mango/Workspace/rss-miner/package/src/rss_miner/storage.py
# Compiled at: 2017-05-14 13:30:12
# Size of source mod 2**32: 947 bytes
from tinydb_serialization import SerializationMiddleware
from time import struct_time
import time
from tinydb_serialization import Serializer

class DateTimeSerializer(Serializer):
    OBJ_CLASS = struct_time

    def encode(self, obj):
        return time.strftime('%Y-%m-%dT%H:%M:%S %Z', obj)

    def decode(self, s):
        return time.strptime(s, '%Y-%m-%dT%H:%M:%S %Z')


serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

def insert_entry(entry, db):
    """Extract and store required information in db"""
    data = {'feed_id':'foo', 
     'title':entry.title, 
     'id':entry.id, 
     'link':entry.link, 
     'published':entry.published, 
     'published_parsed':entry.published_parsed, 
     'authors':entry.get('authors'), 
     'tags':entry.get('tags')}
    db.table('entries').insert(data)