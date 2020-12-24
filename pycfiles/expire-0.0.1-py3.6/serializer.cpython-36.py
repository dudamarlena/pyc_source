# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/expire/serializer.py
# Compiled at: 2018-03-05 19:57:31
# Size of source mod 2**32: 1446 bytes
from expire.base_cache import BaseSerializer
try:
    import ujson as json
except ImportError:
    import json

try:
    import cPickle as pickle
except ImportError:
    import pickle

class JsonSerializer(BaseSerializer):

    def dumps(self, value, **kwargs):
        """
        Serialize the value
        :param value: dict
        :return: string
        """
        if value is not None:
            return json.dumps(value)
        else:
            return ''

    def loads(self, value, **kwargs):
        """
        Deserialize the value
        :param value: string
        :return: dict
        """
        if value is not None:
            return json.loads(value)
        else:
            return {}


class PickleSerializer(BaseSerializer):

    def dumps(self, value, **kwargs):
        """
        Serialize the value
        :param value: object
        :return: bytes
        """
        return pickle.dumps(value)

    def loads(self, value, **kwargs):
        """
        Deserialize the value
        :param value: bytes
        :return: object
        """
        if value is not None:
            return pickle.loads(value)
        else:
            return value


class StrSerializer(BaseSerializer):

    def dumps(self, value, **kwargs):
        """
        Serialize the value
        :param value: str
        :return: str
        """
        return value

    def loads(self, value, **kwargs):
        """
        Deserialize the value
        :param value: str
        :return: str
        """
        return value