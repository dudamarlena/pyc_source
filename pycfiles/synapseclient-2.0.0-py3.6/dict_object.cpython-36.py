# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/core/models/dict_object.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 769 bytes
import collections, json

class DictObject(dict):

    @classmethod
    def getByNameURI(cls, name):
        print("%s can't be retrieved by name" % cls)
        raise ValueError

    def __init__(self, *args, **kwargs):
        self.__dict__ = self
        for arg in args:
            if isinstance(arg, collections.Mapping):
                self.__dict__.update(arg)

        self.__dict__.update(kwargs)

    def __str__(self):
        return json.dumps(self, sort_keys=True, indent=2)

    def json(self, ensure_ascii=True):
        return json.dumps(self, sort_keys=True, indent=2, ensure_ascii=ensure_ascii)