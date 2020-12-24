# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/cache/storage.py
# Compiled at: 2006-08-02 05:57:50
import cPickle
try:
    import memcache
except (ImportError,):
    memcache = None

try:
    import dbm
except (ImportError,):
    dbm = None

class MemoryStorage(dict):
    """ Simple in-memory storage type """
    __module__ = __name__


class MemCachedStorage(object):
    """ Storage type using MemCached server

    @param servers sequence of host addresses and ports
    @param debug debug flag passed to memcache.Client 
    """
    __module__ = __name__

    def __init__(self, servers, debug=0):
        if not memcache:
            raise RuntimeError('Memcache client module not available')
        self.client = memcache.Client(servers, debug)

    def get(self, key, default=None):
        return self.client.get_multi([key]).get(key, default)

    def __getitem__(self, key):
        key = str(hash(key))
        return self.client.get_multi([key])[key]

    def __setitem__(self, key, value):
        key = str(hash(key))
        return self.client.set(key, value, value.ttl)

    def __delitem__(self, key):
        return self.client.delete(key)

    def keys(self):
        return ()

    def items(self):
        return ()

    def values(self):
        return ()

    @classmethod
    def factory(cls, servers, debug):
        """ creates a callable to construct instances with given arguments

        @param servers sequence of host addresses and ports
        @param debug debug flag passed to memcache.Client
        @return factory function that creates storage instances
        """

        def inner():
            return cls(servers, debug)

        return inner


class DbmStorage(object):
    """ Storage type using dbm object with pickled values
    
    @param database filename 
    @param flag one of 'r', 'w', 'c', or 'n'
    @param mode file mode
    """
    __module__ = __name__

    def __init__(self, filename, flag, mode):
        self.client = dbm.open(filename, flag, mode)

    def get(self, key, default=None):
        key = str(key)
        return cPickle.loads(self.client.get(key, default))

    def __getitem__(self, key):
        key = str(key)
        return cPickle.loads(self.client[key])

    def __setitem__(self, key, value):
        key = str(key)
        self.client[key] = cPickle.dumps(value)

    def __delitem__(self, key):
        key = str(key)
        del self.client[key]

    def keys(self):
        return self.client.keys()

    def items(self):
        return self.client.items()

    def values(self):
        return self.client.values()

    @classmethod
    def factory(cls, filename, flag, mode):
        """ creates a callable to construct instances with given arguments

        @param database filename 
        @param flag one of 'r', 'w', 'c', or 'n'
        @param mode file mode
        @return factory function that creates storage instances
        """

        def inner():
            return cls(filename, flag, mode)

        return inner