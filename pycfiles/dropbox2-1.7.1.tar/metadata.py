# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rick/workspace/dropbox/dropbox/metadata.py
# Compiled at: 2013-09-20 14:09:53
from dateutil import parser

class Metadata(object):

    def key_map(self, key, value):
        mapper = self.KEY_MAPPING.get(key, lambda self, v: v)
        value = mapper(self, value)
        return self.type_map(value)

    def type_map(self, value):
        mapper = self.TYPE_MAPPING.get(type(value), lambda self, v: v)
        value = mapper(self, value)
        return value

    def convert_timestamp(self, timestamp):
        return parser.parse(timestamp)

    def convert_list(self, list_):
        return MetadataList(list_)

    def convert_dict(self, dict_):
        return MetadataDict(dict_)

    KEY_MAPPING = {'modified': convert_timestamp, 
       'client_mtime': convert_timestamp}
    TYPE_MAPPING = {dict: convert_dict, 
       list: convert_list}


class MetadataDict(dict, Metadata):

    def __init__(self, metadata):
        for key, value in metadata.iteritems():
            self[key] = self.key_map(key, value)

    def __getattr__(self, key):
        if key in self:
            return self[key]
        raise AttributeError('No such attribute %r' % key)


class MetadataList(list, Metadata):

    def __init__(self, metadata):
        for value in metadata:
            self.append(self.type_map(value))