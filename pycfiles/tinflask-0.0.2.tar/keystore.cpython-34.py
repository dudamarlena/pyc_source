# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jr/GoogleDrive/Dev/python/tinflask/tinflask/keystore.py
# Compiled at: 2015-03-06 17:50:10
# Size of source mod 2**32: 2976 bytes
from tinflask import etcd

class KeyStore(object):
    __doc__ = 'Store/cache for public/private key pairs for endpoint signing.\n    '

    def __init__(self, key, config):
        """Creates a new key store for the given key and configuration.
        """
        self.key = key
        self.private_key = None
        self._keys = {}
        self._config = config

    def has_key(self, key):
        """Returns wether the given key is present in the store.
        """
        return key in self._keys

    def keys(self):
        """Returns a list of all keys within the store.
        """
        return list(self._keys)

    def get(self, key):
        """Gets the private key for the given key.
        """
        return self._keys.get(key)

    def load_keys(self):
        """Not Implemented.
        """
        pass

    def load_private_key(self):
        """Not Implemented.
        """
        pass


class File(KeyStore):
    __doc__ = 'Configuration file backed KeyStore.\n\n    load functions are side effect free.\n    '

    def __init__(self, key, config):
        """Reads private and public keys from configuration file based on environment.
        """
        super(File, self).__init__(key, config)
        self._keys = self._config.get('authorizedKeys', {})
        self.private_key = self._config.get('privateKey')


class ETCD(KeyStore):
    __doc__ = 'Etcd backed KeyStore.\n    '

    def __init__(self, key, config, etcd_url):
        """Creates a new etcd backed KeyStore.
        """
        super(ETCD, self).__init__(key, config)
        self._etcd_url = etcd_url
        self.load_private_key()
        self.load_keys()

    def get_etcd(self, key):
        """Returns the the private key from etcd directly.
        """
        url = '%s/%s' % (self._etcd_url, key)
        private_key = etcd.private_key(url)
        return private_key

    def get(self, key):
        """Lazy loads the matching private_key for the given public key.
        """
        private_key = self._keys.get(key, -1)
        if private_key == -1:
            return
        if private_key != '':
            return private_key
        private_key = self.get_etcd(key)
        self._keys[key] = private_key
        return private_key

    def load_keys(self):
        """Loads authorized public keys from etcd.
        """
        url = '%s/%s' % (self._etcd_url, self.key)
        try:
            self._keys = etcd.authorized_keys(url)
        except Exception as ex:
            print(ex)

    def load_private_key(self):
        """Loads private key from etcd.
        """
        url = '%s/%s' % (self._etcd_url, self.key)
        try:
            self.private_key = etcd.private_key(url)
        except Exception as ex:
            print(ex)