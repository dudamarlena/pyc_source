# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\fabric\caching.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 9413 bytes
"""Implementing caching mechanisms for MySQL Fabric"""
import bisect
from datetime import datetime, timedelta
from hashlib import sha1
import logging, threading
from . import FabricShard
_LOGGER = logging.getLogger('myconnpy-fabric')
_CACHE_TTL = 60

def insort_right_rev(alist, new_element, low=0, high=None):
    """Similar to bisect.insort_right but for reverse sorted lists

    This code is similar to the Python code found in Lib/bisect.py.
    We simply change the comparison from 'less than' to 'greater than'.
    """
    if low < 0:
        raise ValueError('low must be non-negative')
    if high is None:
        high = len(alist)
    while low < high:
        middle = (low + high) // 2
        if new_element > alist[middle]:
            high = middle
        else:
            low = middle + 1

    alist.insert(low, new_element)


class CacheEntry(object):
    __doc__ = 'Base class for MySQL Fabric cache entries'

    def __init__(self, version=None, fabric_uuid=None, ttl=_CACHE_TTL):
        self.version = version
        self.fabric_uuid = fabric_uuid
        self.last_updated = datetime.utcnow()
        self._ttl = ttl

    @classmethod
    def hash_index(cls, part1, part2=None):
        """Create hash for indexing"""
        raise NotImplementedError

    @property
    def invalid(self):
        """Returns True if entry is not valid any longer

        This property returns True when the entry is not valid any longer.
        The entry is valid when now > (last updated + ttl), where ttl is
        in seconds.
        """
        if not self.last_updated:
            return False
        else:
            atime = self.last_updated + timedelta(seconds=(self._ttl))
            return datetime.utcnow() > atime

    def reset_ttl(self):
        """Reset the Time to Live"""
        self.last_updated = datetime.utcnow()

    def invalidate(self):
        """Invalidates the cache entry"""
        self.last_updated = None


class CacheShardTable(CacheEntry):
    __doc__ = 'Cache entry for a Fabric sharded table'

    def __init__(self, shard, version=None, fabric_uuid=None):
        if not isinstance(shard, FabricShard):
            raise ValueError('shard argument must be a FabricShard instance')
        super(CacheShardTable, self).__init__(version=version, fabric_uuid=fabric_uuid)
        self.partitioning = {}
        self._shard = shard
        self.keys = []
        self.keys_reversed = []
        if shard.key:
            if shard.group:
                self.add_partition(shard.key, shard.group)

    def __getattr__(self, attr):
        return getattr(self._shard, attr)

    def add_partition(self, key, group):
        """Add sharding information for a group"""
        if self.shard_type == 'RANGE':
            _key = int(key)
        else:
            if self.shard_type == 'RANGE_DATETIME':
                try:
                    if ':' in key:
                        _key = datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
                    else:
                        _key = datetime.strptime(key, '%Y-%m-%d').date()
                except:
                    raise ValueError('RANGE_DATETIME key could not be parsed, was: {0}'.format(key))

            else:
                if self.shard_type == 'RANGE_STRING':
                    _key = key
                else:
                    if self.shard_type == 'HASH':
                        _key = key
                    else:
                        raise ValueError('Unsupported sharding type {0}'.format(self.shard_type))
        self.partitioning[_key] = {'group': group}
        self.reset_ttl()
        bisect.insort_right(self.keys, _key)
        insort_right_rev(self.keys_reversed, _key)

    @classmethod
    def hash_index(cls, part1, part2=None):
        """Create hash for indexing"""
        return sha1(part1.encode('utf-8') + part2.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '{class_}({database}.{table}.{column})'.format(class_=(self.__class__),
          database=(self.database),
          table=(self.table),
          column=(self.column))


class CacheGroup(CacheEntry):
    __doc__ = 'Cache entry for a Fabric group'

    def __init__(self, group_name, servers):
        super(CacheGroup, self).__init__(version=None, fabric_uuid=None)
        self.group_name = group_name
        self.servers = servers

    @classmethod
    def hash_index(cls, part1, part2=None):
        """Create hash for indexing"""
        return sha1(part1.encode('utf-8')).hexdigest()

    def __repr__(self):
        return '{class_}({group})'.format(class_=(self.__class__),
          group=(self.group_name))


class FabricCache(object):
    __doc__ = 'Singleton class for caching Fabric data\n\n    Only one instance of this class can exists globally.\n    '

    def __init__(self, ttl=_CACHE_TTL):
        self._ttl = ttl
        self._sharding = {}
        self._groups = {}
        self._FabricCache__sharding_lock = threading.Lock()
        self._FabricCache__groups_lock = threading.Lock()

    def remove_group(self, entry_hash):
        """Remove cache entry for group"""
        with self._FabricCache__groups_lock:
            try:
                del self._groups[entry_hash]
            except KeyError:
                pass
            else:
                _LOGGER.debug('Group removed from cache')

    def remove_shardtable(self, entry_hash):
        """Remove cache entry for shard"""
        with self._FabricCache__sharding_lock:
            try:
                del self._sharding[entry_hash]
            except KeyError:
                pass

    def sharding_cache_table(self, shard, version=None, fabric_uuid=None):
        """Cache information about a shard"""
        entry_hash = CacheShardTable.hash_index(shard.database, shard.table)
        with self._FabricCache__sharding_lock:
            try:
                entry = self._sharding[entry_hash]
                entry.add_partition(shard.key, shard.group)
            except KeyError:
                entry = CacheShardTable(shard, version=version, fabric_uuid=fabric_uuid)
                self._sharding[entry_hash] = entry

    def cache_group(self, group_name, servers):
        """Cache information about a group"""
        entry_hash = CacheGroup.hash_index(group_name)
        with self._FabricCache__groups_lock:
            try:
                entry = self._groups[entry_hash]
                entry.servers = servers
                entry.reset_ttl()
                _LOGGER.debug('Recaching group {0} with {1}'.format(group_name, servers))
            except KeyError:
                entry = CacheGroup(group_name, servers)
                self._groups[entry_hash] = entry
                _LOGGER.debug('Caching group {0} with {1}'.format(group_name, servers))

    def sharding_search(self, database, table):
        """Search cache for a shard based on database and table"""
        entry_hash = CacheShardTable.hash_index(database, table)
        entry = None
        try:
            entry = self._sharding[entry_hash]
            if entry.invalid:
                _LOGGER.debug('{0} invalidated'.format(entry))
                self.remove_shardtable(entry_hash)
                return
        except KeyError:
            return
        else:
            return entry

    def group_search(self, group_name):
        """Search cache for a group based on its name"""
        entry_hash = CacheGroup.hash_index(group_name)
        entry = None
        try:
            entry = self._groups[entry_hash]
            if entry.invalid:
                _LOGGER.debug('{0} invalidated'.format(entry))
                self.remove_group(entry_hash)
                return
        except KeyError:
            return
        else:
            return entry

    def __repr__(self):
        return '{class_}(groups={nrgroups},shards={nrshards})'.format(class_=(self.__class__),
          nrgroups=(len(self._groups)),
          nrshards=(len(self._sharding)))