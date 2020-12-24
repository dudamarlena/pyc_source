# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/coreinit/db/drivers/redis_driver.py
# Compiled at: 2015-11-19 07:10:11
__doc__ = '\nCopyright (c) 2015 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
from coreinit.db.drivers.cache_interface import CacheInterface
from coreinit.service.mixins.avahi import AutoDiscoverMixin
from coreinit.utils.installer import *
from coreinit.utils.exceptions import *
import random

class Cache(AutoDiscoverMixin, CacheInterface):
    conn = None

    def configure(self):
        super(Cache, self).configure()
        self._autodiscover_configure()
        install_pip(['redis', 'simplejson'])

    def __init__(self):
        self.configure()
        endpoints = self._get_services('cache_redis')
        if len(endpoints) == 0:
            raise ConfigurationException('failed to find cache service')
        import redis
        self.conn = redis.Redis(endpoints[int(random.random() * len(endpoints))][0], socket_keepalive=1)

    def hset(self, name, key, value):
        return self.conn.hset(name, key, value)

    def hget(self, name, key):
        return self.conn.hget(name, key)

    def hdel(self, name, key):
        return self.conn.hdel(name, key)

    def hkeys(self, name):
        return self.conn.hkeys(name)

    def hvals(self, name):
        return self.conn.hvals(name)

    def keys(self):
        return self.conn.keys()

    def delete(self, name):
        return self.conn.delete(name)

    def lock(self, name):
        return self.conn.lock(name)