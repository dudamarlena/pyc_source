# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dataexchange\dataexchange\json\exchange.py
# Compiled at: 2020-01-22 07:07:39
# Size of source mod 2**32: 998 bytes
from dataexchange.json.encoders import jsonencoder
from dataexchange.json.keyrename import list_keyrename
from dataexchange.json.keyrename import dict_keyrename
from dataexchange.json.nesteddict import nested_dict

class JsonExchange(object):

    def __init__(self, data):
        if isinstance(data, str):
            self.data = jsonencoder(data)
        else:
            self.data = data
        self.raw_data = self.data

    def key_rename(self, depth=None, keys=None):
        if keys:
            if isinstance(self.data, list):
                return list_keyrename(self.data, keys)
                if isinstance(self.data, dict):
                    if depth:
                        return nested_dict(self.data, self.raw_data, depth, keys)
                    return dict_keyrename(self.data, keys)
            else:
                return f"{type(self.data)} Data Type is not Accepted."
        else:
            return 'Key(s) not provided.'