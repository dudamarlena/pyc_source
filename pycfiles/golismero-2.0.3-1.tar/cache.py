# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/net/cache.py
# Compiled at: 2014-01-14 18:58:51
"""
Network cache API.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'NetworkCache']
from ..config import Config
from ...common import Singleton
from ...messaging.codes import MessageCode
from collections import defaultdict
from functools import partial

class _NetworkCache(Singleton):
    """
    Cache for network resources, separated by protocol.
    """

    def __init__(self):
        self._clear_local_cache()

    def _clear_local_cache(self):
        """
        .. warning: Do not call!
        """
        self.__cache = defaultdict(partial(defaultdict, dict))

    def get(self, key, protocol):
        """
        Get a network resource from the cache.

        :param key: Key to reference the network resource.
        :type key: str

        :param protocol: Network protocol.
        :type protocol: str

        :returns: Resource from the cache, None if not found.
        :rtype: object | None
        """
        data = self.__cache[Config.audit_name][protocol].get(key, None)
        if data is None:
            data = Config._context.remote_call(MessageCode.MSG_RPC_CACHE_GET, key, protocol)
            if data is not None:
                self.__cache[Config.audit_name][protocol][key] = data
        return data

    def set(self, key, data, protocol, timestamp=None, lifespan=None):
        """
        Store a network resource in the cache.

        :param key: Key to reference the network resource.
        :type key: str

        :param data: Data to store in the cache.
        :type data: object

        :param protocol: Network protocol.
        :type protocol: str

        :param timestamp: Timestamp for this network resource.
        :type timestamp: int

        :param lifespan: Time to live in the cache.
        :type lifespan: int
        """
        self.__cache[Config.audit_name][protocol][key] = data
        Config._context.async_remote_call(MessageCode.MSG_RPC_CACHE_SET, key, protocol, data)

    def remove(self, key, protocol):
        """
        Remove a network resource from the cache.

        :param key: Key to reference the network resource.
        :type key: str

        :param protocol: Network protocol.
        :type protocol: str
        """
        try:
            del self.__cache[Config.audit_name][protocol][key]
        except KeyError:
            pass

        Config._context.async_remote_call(MessageCode.MSG_RPC_CACHE_REMOVE, key, protocol)

    def exists(self, key, protocol):
        """
        Verify if the given key exists in the cache.

        :param key: Key to reference the network resource.
        :type key: str

        :returns: True if the resource is in the cache, False otherwise.
        :rtype: bool
        """
        found = key in self.__cache[Config.audit_name][protocol]
        if not found:
            found = Config._context.remote_call(MessageCode.MSG_RPC_CACHE_CHECK, key, protocol)
            found = bool(found)
        return found


NetworkCache = _NetworkCache()