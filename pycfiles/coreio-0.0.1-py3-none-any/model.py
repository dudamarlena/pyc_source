# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/coreinit/db/model.py
# Compiled at: 2015-11-18 12:57:08
__doc__ = '\nCopyright (c) 2015 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import simplejson, datetime, uuid
from coreinit.db import Cache
from coreinit.utils.exceptions import *

class Model(object):
    id = None
    keys = []
    serializable = []
    container = 'undefined'

    def __init__(self, id=None, data=None):
        if id is not None:
            self.id = id
            data = Cache.hget(self.container, self.cache_key())
            if not data:
                raise DbException('object not found')
        if data is not None:
            deserialized = simplejson.loads(data)
            for key in deserialized:
                setattr(self, key, deserialized[key])
                if key not in self.serializable:
                    self.serializable.append(key)

        else:
            self.id = str(uuid.uuid1())
            self.creation_time = datetime.datetime.now()
        return

    def cache_key(self):
        """
        Returns the key which identifies object in cache
        """
        return '%s:%s' % (self.container, self.id)

    def save(self, skip_lock=False):
        """
        Store object in cache
        """
        l = Cache.lock(self.container + ':' + ':lock')
        if not skip_lock:
            l.acquire()
        d = {}
        for field in self.serializable:
            d[field] = getattr(self, field, None)

        r = simplejson.dumps(d)
        Cache.hset(self.container, self.cache_key(), r)
        for key in self.keys:
            Cache.hset(self.container + ':' + key, self.cache_key(), getattr(self, key))

        if not skip_lock:
            l.release()
        return

    def delete(self, skip_lock=False):
        """
        Delete whole object from cache
        """
        l = Cache.lock(self.container + ':' + ':lock')
        if not skip_lock:
            l.acquire()
        Cache.hdel(self.container, self.cache_key())
        for key in self.keys:
            Cache.hdel(self.container + ':' + key, self.cache_key())

        if not skip_lock:
            l.release()