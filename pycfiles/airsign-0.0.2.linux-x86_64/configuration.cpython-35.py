# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/airsign/configuration.py
# Compiled at: 2016-05-11 05:11:50
# Size of source mod 2**32: 2068 bytes
import os, json, collections
from appdirs import user_data_dir
appname = 'airsign'
appauthor = 'Fabian Schuh'
configFile = 'config.json'

class Configuration(collections.MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))
        self._loadConfig()

    def __getitem__(self, key):
        """ This method behaves differently from regular `dict` in that
            it returns `None` if a key is not found!
        """
        internalKey = self.__keytransform__(key)
        if internalKey in self.store:
            return self.store[internalKey]
        else:
            return

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value
        self._storeConfig()

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]
        self._storeConfig()

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

    def mkdir_p(self, path):
        if os.path.isdir(path):
            return
            try:
                os.makedirs(path)
            except OSError:
                raise

    def _storeConfig(self):
        data_dir = user_data_dir(appname, appauthor)
        f = os.path.join(data_dir, configFile)
        self.mkdir_p(data_dir)
        with open(f, 'w') as (fp):
            json.dump(self.store, fp)

    def _loadConfig(self):
        data_dir = user_data_dir(appname, appauthor)
        f = os.path.join(data_dir, configFile)
        if os.path.isfile(f):
            with open(f, 'r') as (fp):
                try:
                    self.update(json.load(fp))
                    return self
                except:
                    raise ValueError('Error loading configuration :(')

        else:
            return []