# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/database/cachedb.py
# Compiled at: 2014-01-14 18:58:51
"""
Network cache implementations.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'PersistentNetworkCache', 'VolatileNetworkCache']
from .common import BaseDB, atomic, transactional
from ..common import get_user_settings_folder
from ..managers.rpcmanager import implementor
from ..messaging.codes import MessageCode
from collections import defaultdict
from functools import partial
from os.path import join
sqlite3 = None

@implementor(MessageCode.MSG_RPC_CACHE_GET)
def rpc_cache_get(orchestrator, audit_name, *args, **kwargs):
    return orchestrator.cacheManager.get(audit_name, *args, **kwargs)


@implementor(MessageCode.MSG_RPC_CACHE_SET)
def rpc_cache_set(orchestrator, audit_name, *args, **kwargs):
    return orchestrator.cacheManager.set(audit_name, *args, **kwargs)


@implementor(MessageCode.MSG_RPC_CACHE_CHECK)
def rpc_cache_check(orchestrator, audit_name, *args, **kwargs):
    return orchestrator.cacheManager.exists(audit_name, *args, **kwargs)


@implementor(MessageCode.MSG_RPC_CACHE_REMOVE)
def rpc_cache_remove(orchestrator, audit_name, *args, **kwargs):
    return orchestrator.cacheManager.remove(audit_name, *args, **kwargs)


class BaseNetworkCache(BaseDB):
    """
    Abtract class for network cache databases.
    """

    @staticmethod
    def _sanitize_protocol(protocol):
        protocol = protocol.lower()
        if '://' in protocol:
            protocol = protocol[:protocol.find('://')]
        return protocol

    def get(self, audit, key, protocol='http'):
        """
        Get a network resource from the cache.

        :param key: key to reference the network resource
        :type key: str

        :param protocol: network protocol
        :type protocol: str

        :returns: object -- resource from the cache | None
        """
        raise NotImplementedError('Subclasses MUST implement this method!')

    def set(self, audit, key, data, protocol='http', timestamp=None, lifespan=None):
        """
        Store a network resource in the cache.

        :param key: key to reference the network resource
        :type key: str

        :param data: data to store in the cache
        :type data: object

        :param protocol: network protocol
        :type protocol: str

        :param timestamp: timestamp for this network resource
        :type timestamp: int

        :param lifespan: time to live in the cache
        :type lifespan: int
        """
        raise NotImplementedError('Subclasses MUST implement this method!')

    def remove(self, audit, key, protocol='http'):
        """
        Remove a network resource from the cache.

        :param key: key to reference the network resource
        :type key: str

        :param protocol: network protocol
        :type protocol: str
        """
        raise NotImplementedError('Subclasses MUST implement this method!')

    def exists(self, audit, key, protocol='http'):
        """
        Verify if the given key exists in the cache.

        :param key: key to reference the network resource
        :type key: str

        :returns: True if the resource is in the cache, False otherwise.
        """
        raise NotImplementedError('Subclasses MUST implement this method!')

    def clean(self, audit):
        """
        Delete all cache entries for the given audit.

        :param audit: Audit name.
        :type audit: str
        """
        raise NotImplementedError('Subclasses MUST implement this method!')


class VolatileNetworkCache(BaseNetworkCache):
    """
    In-memory cache for network resources, separated by protocol.
    """

    def __init__(self):
        self.__cache = defaultdict(partial(defaultdict, dict))

    def get(self, audit, key, protocol='http'):
        protocol = self._sanitize_protocol(protocol)
        return self.__cache[audit][protocol].get(key, None)

    def set(self, audit, key, data, protocol='http', timestamp=None, lifespan=None):
        protocol = self._sanitize_protocol(protocol)
        self.__cache[audit][protocol][key] = data

    def remove(self, audit, key, protocol='http'):
        protocol = self._sanitize_protocol(protocol)
        try:
            del self.__cache[audit][protocol][key]
        except KeyError:
            pass

    def exists(self, audit, key, protocol='http'):
        protocol = self._sanitize_protocol(protocol)
        return key in self.__cache[audit][protocol]

    def clean(self, audit):
        self.__cache[audit] = defaultdict(dict)

    def close(self):
        self.__cache = defaultdict(partial(defaultdict, dict))

    def dump(self, filename):
        pass


class PersistentNetworkCache(BaseNetworkCache):
    """
    Network cache with a database backend.
    """

    def __init__(self):
        global sqlite3
        filename = join(get_user_settings_folder(), 'cache.db')
        if sqlite3 is None:
            import sqlite3
        self.__db = sqlite3.connect(filename)
        self.__cursor = None
        self.__busy = False
        self.__create()
        return

    def _atom(self, fn, args, kwargs):
        if self.__busy:
            raise RuntimeError('The database is busy')
        try:
            self.__busy = True
            return fn(self, *args, **kwargs)
        finally:
            self.__busy = False

    def _transaction(self, fn, args, kwargs):
        if self.__busy:
            raise RuntimeError('The database is busy')
        try:
            self.__busy = True
            self.__cursor = self.__db.cursor()
            try:
                retval = fn(self, *args, **kwargs)
                self.__db.commit()
                return retval
            except:
                self.__db.rollback()
                raise

        finally:
            self.__cursor = None
            self.__busy = False

        return

    @transactional
    def __create(self):
        """
        Create the database schema if needed.
        """
        self.__cursor.execute('\n            CREATE TABLE IF NOT EXISTS cache (\n                id INTEGER PRIMARY KEY,\n                audit STRING NOT NULL,\n                protocol STRING NOT NULL,\n                key STRING NOT NULL,\n                timestamp INTEGER NOT NULL\n                          DEFAULT CURRENT_TIMESTAMP,\n                lifespan INTEGER NOT NULL\n                         DEFAULT 0,\n                data BLOB NOT NULL,\n\n                UNIQUE (audit, protocol, key) ON CONFLICT REPLACE\n            );\n        ')

    @transactional
    def get(self, audit, key, protocol='http'):
        protocol = self._sanitize_protocol(protocol)
        self.__cursor.execute('\n            SELECT data FROM cache\n            WHERE audit = ? AND key = ? AND protocol = ?\n                AND (timestamp = 0 OR lifespan = 0 OR\n                     timestamp + lifespan > CURRENT_TIMESTAMP\n                )\n            LIMIT 1;\n        ', (audit, key, protocol))
        row = self.__cursor.fetchone()
        if row is not None:
            return self.decode(row[0])
        else:
            return

    @transactional
    def set(self, audit, key, data, protocol='http', timestamp=None, lifespan=None):
        protocol = self._sanitize_protocol(protocol)
        data = self.encode(data)
        data = sqlite3.Binary(data)
        if lifespan is None:
            lifespan = 0
        if timestamp is None:
            self.__cursor.execute('\n                INSERT INTO cache (audit, key, protocol, data, lifespan)\n                VALUES            (  ?,    ?,     ?,       ?,     ?    );\n            ', (audit, key, protocol, data, lifespan))
        else:
            self.__cursor.execute('\n                INSERT INTO cache (audit, key, protocol, data, timestamp, lifespan)\n                VALUES            (  ?,    ?,     ?,       ?,      ?,        ?    );\n            ', (audit, key, protocol, data, timestamp, lifespan))
        return

    @transactional
    def remove(self, audit, key, protocol='http'):
        protocol = self._sanitize_protocol(protocol)
        self.__cursor.execute('\n            DELETE FROM cache\n            WHERE audit = ? AND key = ? AND protocol = ?;\n        ', (audit, key, protocol))

    @transactional
    def exists(self, audit, key, protocol='http'):
        protocol = self._sanitize_protocol(protocol)
        self.__cursor.execute('\n            SELECT COUNT(id) FROM cache\n            WHERE audit = ? AND key = ? AND protocol = ?\n                AND (timestamp = 0 OR lifespan = 0 OR\n                     timestamp + lifespan > CURRENT_TIMESTAMP\n                )\n            LIMIT 1;\n        ', (audit, key, protocol))
        return bool(self.__cursor.fetchone()[0])

    @transactional
    def clean(self, audit):
        self.__cursor.execute('\n            DELETE FROM cache\n            WHERE audit = ?;\n        ', (audit,))

    def compact(self):
        try:
            self.__clear_old_entries()
            self.__vacuum()
        except sqlite3.Error:
            pass

    @transactional
    def __clear_old_entries(self):
        self.__cursor.execute('\n            DELETE FROM cache\n                WHERE timestamp != 0 AND lifespan != 0 AND\n                      timestamp + lifespan <= CURRENT_TIMESTAMP;\n        ')

    @transactional
    def __vacuum(self):
        self.__cursor.execute('VACUUM;')

    @atomic
    def dump(self, filename):
        with open(filename, 'w') as (f):
            for line in self.__db.iterdump():
                f.write(line + '\n')

    @atomic
    def close(self):
        try:
            self.__db.close()
        except Exception:
            pass