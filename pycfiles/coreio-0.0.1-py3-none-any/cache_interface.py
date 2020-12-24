# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/coreinit/db/drivers/cache_interface.py
# Compiled at: 2015-11-18 12:57:08
__doc__ = '\nCopyright (c) 2015 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'

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