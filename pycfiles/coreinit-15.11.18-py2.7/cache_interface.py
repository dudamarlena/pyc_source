# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/coreinit/db/drivers/cache_interface.py
# Compiled at: 2015-11-18 12:57:08
"""
Copyright (c) 2015 Maciej Nabozny

This file is part of CloudOver project.

CloudOver is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

class CacheInterface(object):

    def configure(self):
        pass

    def hset(self, name, key, value):
        """
        Set value for hash map in name element
        """
        raise Exception('not implemented')

    def hget(self, name, key):
        """
        Get value of hash map in name element
        """
        raise Exception('not implemented')

    def hdel(self, name, key):
        """
        Delete item in hash map by given key
        """
        raise Exception('not implemented')

    def hkeys(self, name):
        """
        Return list of keys from given hash map
        """
        raise Exception('not implemented')

    def hvals(self, name):
        """
        Return list of values from given hash map
        """
        raise Exception('not implemented')

    def keys(self):
        """
        List all keys in cache (containers)
        """
        raise Exception('not implemented')

    def delete(self, name):
        """
        Delete Cache key by name (container)
        """
        raise Exception('not implemented')

    def lock(self, name):
        raise Exception('not implemented')