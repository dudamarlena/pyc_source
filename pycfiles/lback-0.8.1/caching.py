# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mysql\connector\fabric\caching.pyc
# Compiled at: 2014-07-26 22:44:23
"""Implementing caching mechanisms for MySQL Fabric"""
from datetime import datetime, timedelta
from hashlib import sha1
import logging
from . import FabricShard
_LOGGER = logging.getLogger('myconnpy-fabric')
_CACHE_TTL = 60

def refresh_ttl(func):
    """Decorator updating the TTL of CacheEntry"""

    def wrapper(self, *args, **kwargs):
        """Decorator wrapper"""
        func(self, *args, **kwargs)
        self.last_updated = datetime.utcnow()

    return wrapper


class CacheEntry(object):
    """Base class for MySQL Fabric cache entries"""

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
        atime = self.last_updated + timedelta(seconds=self._ttl)
        return datetime.utcnow() > atime

    def invalidate(self):
        """Invalidates the cache entry"""
        self.last_updated = None
        return


class CacheShardTable(CacheEntry):
    """Cache entry for a Fabric sharded table"""

    def __init__(self, shard, version=None, fabric_uuid=None):
        if not isinstance(shard, FabricShard):
            ValueError('shard argument must be a FabricShard instance')
        super(CacheShardTable, self).__init__(version=version, fabric_uuid=fabric_uuid)
        self.partitioning = {}
        self._shard = shard
        if shard.key and shard.group:
            self.add_partition(shard.key, shard.group)

    def __getattr__(self, attr):
        return getattr(self._shard, attr)

    @refresh_ttl
    def add_partition(self, key, group):
        """Add sharding information for a group"""
        if self.shard_type == 'RANGE':
            key = int(key)
        self.partitioning[key] = {'group': group}

    @classmethod
    def hash_index(cls, part1, part2=None):
        """Create hash for indexing"""
        return sha1(part1.encode('utf-8') + part2.encode('utf-8')).hexdigest()

    def __repr__(self):
        return ('{class_}({database}.{table}.{column})').format(class_=self.__class__, database=self.database, table=self.table, column=self.column)


class CacheGroup(CacheEntry):
    """Cache entry for a Fabric group"""

    def __init__(self, group_name, servers):
        super(CacheGroup, self).__init__(version=None, fabric_uuid=None)
        self.group_name = group_name
        self.servers = servers
        return

    @classmethod
    def hash_index(cls, part1, part2=None):
        """Create hash for indexing"""
        return sha1(part1.encode('utf-8')).hexdigest()

    def __repr__(self):
        return ('{class_}({group})').format(class_=self.__class__, group=self.group_name)


class FabricCache(object):
    """Singleton class for caching Fabric data

    Only one instance of this class can exists globally.
    """

    def __init__(self, ttl=_CACHE_TTL):
        self._ttl = ttl
        self._sharding = {}
        self._groups = {}

    def sharding_cache_table(self, shard, version=None, fabric_uuid=None):
        """Cache information about a shard"""
        entry_hash = CacheShardTable.hash_index(shard.database, shard.table)
        try:
            entry = self._sharding[entry_hash]
            entry.add_partition(shard.key, shard.group)
        except KeyError:
            entry = CacheShardTable(shard, version=version, fabric_uuid=fabric_uuid)
            self._sharding[entry_hash] = entry

    def cache_group(self, group_name, servers):
        """Cache information about a group"""
        entry_hash = CacheGroup.hash_index(group_name)
        try:
            _LOGGER.debug(('Recaching group {0} with {1}').format(group_name, servers))
            entry = self._groups[entry_hash]
            entry.servers = servers
        except KeyError:
            entry = CacheGroup(group_name, servers)
            self._groups[entry_hash] = entry

    def sharding_search(self, database, table):
        """Search cache for a shard based on database and table"""
        entry_hash = CacheShardTable.hash_index(database, table)
        entry = None
        try:
            entry = self._sharding[entry_hash]
            if entry.invalid:
                _LOGGER.debug(('{entry} invalidated').format(entry))
                return
        except KeyError:
            return

        return entry

    def group_search(self, group_name):
        """Search cache for a group based on its name"""
        entry_hash = CacheGroup.hash_index(group_name)
        entry = None
        try:
            entry = self._groups[entry_hash]
            if entry.invalid:
                _LOGGER.debug(('{entry} invalidated').format(entry))
                return
        except KeyError:
            return

        return entry

    def __repr__(self):
        return ('{class_}(groups={nrgroups},shards={nrshards})').format(class_=self.__class__, nrgroups=len(self._groups), nrshards=len(self._sharding))