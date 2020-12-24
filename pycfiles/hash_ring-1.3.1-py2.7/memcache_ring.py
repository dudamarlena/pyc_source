# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/hash_ring/memcache_ring.py
# Compiled at: 2012-12-14 20:14:49
import memcache, types
from hash_ring import HashRing

class MemcacheRing(memcache.Client):
    """Extends python-memcache so it uses consistent hashing to
    distribute the keys.
    """

    def __init__(self, servers, *k, **kw):
        self.hash_ring = HashRing(servers)
        memcache.Client.__init__(self, servers, *k, **kw)
        self.server_mapping = {}
        for server_uri, server_obj in zip(servers, self.servers):
            self.server_mapping[server_uri] = server_obj

    def _get_server(self, key):
        if type(key) == types.TupleType:
            return memcache.Client._get_server(key)
        else:
            for i in range(self._SERVER_RETRIES):
                iterator = self.hash_ring.iterate_nodes(key)
                for server_uri in iterator:
                    server_obj = self.server_mapping[server_uri]
                    if server_obj.connect():
                        return (server_obj, key)

            return (None, None)