# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parsimony/persistence/in_memory.py
# Compiled at: 2014-12-21 10:46:54
# Size of source mod 2**32: 1426 bytes
import pickle
from . import Cache

class MemCache(Cache):
    __doc__ = 'Parameter Cache that will bring parameters from a store into local memory if it exists and persist updates to\n    the store.\n    '

    def __init__(self, store):
        """Initialize by reading from the store

        :param: Store object
        """
        self._store = store
        try:
            self._store_data = self._store.read()
        except IOError:
            self._store_data = {}

        super().__init__()

    def __contains__(self, key):
        return key in self._store_data

    def __delitem__(self, key):
        del self._store_data[key]
        self._store.write(self._store_data)

    def parameter_keys(self, key):
        if key in list(self._store_data.keys()):
            return self._store_data[key]['parameters']
        return {}

    def compare(self, value, parameter_key):
        return value == self._store_data[parameter_key]['value']

    def update(self, key, value, parameter_keys=None):
        """Update the memory cache and store

        :param key: key of object to store
        :param value: value of object to store
        :param parameter_keys: keys for generator parameters
        """
        self._store_data[key] = {'parameters': parameter_keys,  'value': value}
        self._store.write(self._store_data)