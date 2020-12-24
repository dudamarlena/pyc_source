# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aarontraas/workspace/personal/Clash-Royale-Clan-Tools/crtools/models/dictable.py
# Compiled at: 2019-09-27 12:13:04
# Size of source mod 2**32: 949 bytes
import json

class Dictable:

    def __init__(self, attribute_map):
        self.attribute_map = attribute_map

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}
        for attr_name, attr_type in self.attribute_map.items():
            value = getattr(self, attr_name)
            if isinstance(value, list):
                result[attr] = list(map(lambda x:                 if hasattr(x, 'to_dict'):
x.to_dict() # Avoid dead code: x, value))
            elif hasattr(value, 'to_dict'):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(lambda item:                 if hasattr(item[1], 'to_dict'):
(item[0], item[1].to_dict()) # Avoid dead code: item, value.items()))
            else:
                result[attr] = value

        return result