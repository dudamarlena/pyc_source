# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/pyenv/uvena_de/django_clear_memcache/utility.py
# Compiled at: 2017-04-17 10:26:28
# Size of source mod 2**32: 3547 bytes
from logging import getLogger
import re, telnetlib
TELNET_READ_TIMEOUT = 1.0

class MemcachedUtility(object):
    __doc__ = '\n    A small utility to control a memcached server via its telnet interface.\n    '
    _key_regex = re.compile('ITEM (.*) \\[(.*); (.*)\\]')
    _slab_regex = re.compile('STAT items:(.*):number')
    _stat_regex = re.compile('STAT (.*) (.*)\\r')

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._client = None
        self._logger = getLogger('djago_memcache_clear')

    def open(self):
        if self._client is None:
            self._client = telnetlib.Telnet(self._host, self._port)

    def close(self):
        if self._client is not None:
            self._client.close()

    def command(self, cmd, read_until='END'):
        """Write a command to telnet and return the response"""
        self._logger.debug('[%12s] executing memcache command(%-10s): %s', self._host, repr(read_until), cmd)
        command = '{}\n'.format(cmd)
        self._client.write(command.encode())
        read_until_bytes = read_until.encode()
        response = self._client.read_until(read_until_bytes, TELNET_READ_TIMEOUT)
        return response.decode()

    def key_details(self, sort=True, limit=100):
        """Return a list of tuples containing keys and details"""
        cmd = 'stats cachedump {} {}'
        keys = [key for id_ in self.slab_ids() for key in self._key_regex.findall(self.command(cmd.format(id_, limit)))]
        if sort:
            return sorted(keys)
        return keys

    def get(self, key):
        """Retrieve a single key"""
        return self.command('get {}'.format(key))

    def flush(self):
        """Retrieve a single key"""
        return self.command('flush_all', read_until='OK')

    def keys(self, sort=True, limit=100):
        """Return a list of keys in use"""
        return [key[0] for key in self.key_details(sort=sort, limit=limit)]

    def slab_ids(self):
        """Return a list of slab ids in use"""
        return self._slab_regex.findall(self.command('stats items'))

    def stats(self):
        """Return a dict containing memcached stats"""
        return dict(self._stat_regex.findall(self.command('stats')))

    def delete(self, key):
        result = self.command(('delete {}'.format(key)), read_until='\n')
        result = result.strip()
        self._logger.debug('Delete for key %s returned: %s', key, result)