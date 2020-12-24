# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/server_cache.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 3322 bytes
import errno
from . import log

class StaticCache:
    SERVER_CLASS = None
    SERVER_KWDS = {}
    CACHE = None

    @classmethod
    def cache(cls):
        if not cls.CACHE:
            cls.CACHE = ServerCache((cls.SERVER_CLASS), **cls.SERVER_KWDS)
        return cls.CACHE

    @classmethod
    def close_all(cls):
        if cls.CACHE:
            cls.CACHE.close_all()
            cls.CACHE = None


class ServerCache:
    __doc__ = "\n    A class that caches servers by key so you don't keep closing and re-opening\n    the same server and interrupting your connection.\n\n    The exact nature of the key depends on the sort of server.\n    For example, for a server socket like SimPixel, it would be just a port\n    number, whereas for a UDP connection like Art-Net, it would be a\n    port, ip_address pair.\n    "

    def __init__(self, constructor, **kwds):
        """
        :param constructor: a function which takes a key and some keywords,
            and returns a new server
        :param kwds: keywords to the ``constructor`` function
        """
        self.servers = {}
        self.constructor = constructor
        self.kwds = kwds

    def get_server(self, key, **kwds):
        """
        Get a new or existing server for this key.

        :param int key: key for the server to use
        """
        kwds = dict((self.kwds), **kwds)
        server = self.servers.get(key)
        if server:
            server.check_keywords(self.constructor, kwds)
        else:
            server = _CachedServer(self.constructor, key, kwds)
            self.servers[key] = server
        return server

    def close(self, key):
        server = self.servers.pop(key, None)
        if server:
            server.server.close()
            return True

    def close_all(self):
        for key in list(self.servers.keys()):
            self.close(key)


class _CachedServer:

    def __init__(self, constructor, key, kwds):
        try:
            self.server = constructor(key, **kwds)
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                e.strerror += ADDRESS_IN_USE_ERROR.format(key)
                e.args = (e.errno, e.strerror)
            raise

        self.key = key
        self.constructor = constructor
        self.kwds = kwds

    def check_keywords(self, constructor, kwds):
        if self.constructor != constructor:
            raise ValueError(CACHED_SERVER_ERROR.format(key=(self.key),
              new_type=(str(constructor)),
              old_type=(str(self.constructor))))
        if self.kwds != kwds:
            log.warning(CACHED_KWDS_WARNING.format(server=self, kwds=kwds))

    def close(self):
        pass

    def __getattr__(self, key):
        return getattr(self.server, key)


ADDRESS_IN_USE_ERROR = '\n\nCached server {0} on your machine is already in use.\nPerhaps BiblioPixel is already running on your machine?\n'
CACHED_SERVER_ERROR = '\nTried to open server of type {new_type} on {port}, but there was already\na server of type {old_type} running there.\n'
CACHED_KWDS_WARNING = '\nCached server for {server.port} had keywords {server.kwds},\nbut keywords {kwds} were requested.\n'