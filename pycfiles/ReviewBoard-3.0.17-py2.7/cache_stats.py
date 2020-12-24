# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/cache_stats.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging, socket
from django.conf import settings
from djblets.cache.forwarding_backend import DEFAULT_FORWARD_CACHE_ALIAS
logger = logging.getLogger(__name__)

def get_memcached_hosts():
    """Return the hosts currently configured for memcached.

    Returns:
        list of unicode:
        A list of memcached hostnames or UNIX paths.
    """
    cache_info = settings.CACHES[DEFAULT_FORWARD_CACHE_ALIAS]
    backend = cache_info[b'BACKEND']
    locations = cache_info.get(b'LOCATION', [])
    if b'memcached' not in backend or not locations:
        locations = []
    elif not isinstance(locations, list):
        locations = [
         locations]
    return locations


def get_has_cache_stats():
    """Return whether or not cache stats are supported.

    Returns:
        bool:
        ``True`` if cache stats are supported for the current cache setup.
        ``False`` if cache stats are not supported.
    """
    return len(get_memcached_hosts()) > 0


def get_cache_stats():
    """Return statistics for all supported cache backends.

    This only supports memcached backends.

    Returns:
        list of tuple:
        Each list item corresponds to one configured memcached server.
        The item is a tuple in the form of ``(hostname, stats)``, where
        ``stats`` is a dictionary with statistics from the cache server.

        If no memcached servers are configured, this will return ``None``
        instead.
    """
    hostnames = get_memcached_hosts()
    if not hostnames:
        return None
    else:
        all_stats = []
        for hostname in hostnames:
            try:
                host, port = hostname.split(b':')
            except ValueError:
                socket_af = socket.AF_INET
                host = hostname
                port = 11211

            if host == b'unix':
                socket_af = socket.AF_UNIX
                connect_param = port
            else:
                socket_af = socket.AF_INET
                connect_param = (host, int(port))
            s = socket.socket(socket_af, socket.SOCK_STREAM)
            try:
                s.connect(connect_param)
            except socket.error:
                logger.error(b'Unable to connect to "%s"' % hostname)
                s.close()
                continue

            s.send(b'stats\r\n')
            data = s.recv(2048).decode(b'ascii')
            s.close()
            stats = {}
            for line in data.splitlines():
                info = line.split(b' ')
                if info[0] == b'STAT' and len(info) == 3:
                    try:
                        value = int(info[2])
                    except ValueError:
                        value = info[2]

                    stats[info[1]] = value

            if stats[b'cmd_get'] == 0:
                stats[b'hit_rate'] = 0
                stats[b'miss_rate'] = 0
            else:
                stats[b'hit_rate'] = 100 * stats[b'get_hits'] / stats[b'cmd_get']
                stats[b'miss_rate'] = 100 * stats[b'get_misses'] / stats[b'cmd_get']
            all_stats.append((hostname, stats))

        return all_stats