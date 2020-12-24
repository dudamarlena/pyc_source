# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/object_pool.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 4803 bytes
from weakref import WeakValueDictionary
import threading, multiprocessing, logging
logger = logging.getLogger(__name__)
from ..support.utils import get_new_uuid

class ObjectPool(object):
    __doc__ = '\n        This class allows to fetch mvc model objects using their UUID.\n        This requires to model to have a property called "uuid". All\n        class inheriting from the base \'Model\' class will have this.\n        If implementing a custom model, the UUID property is responsible\n        for the removal and addition to the pool when it changes values.\n        Also see the UUIDProperty descriptor for an example implementation.\n        We can use this to store complex relations between objects where \n        references to each other can be replaced with the UUID.\n        For a multi-threaded version see ThreadedObjectPool. \n    '

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self._objects = WeakValueDictionary()

    def add_or_get_object(self, obj):
        try:
            self.add_object(obj, force=False, silent=False)
            return obj
        except KeyError:
            return self.get_object(obj.uuid)

    def add_object(self, obj, force=False, fail_on_duplicate=False):
        if obj.uuid not in self._objects or force:
            self._objects[obj.uuid] = obj
        else:
            if fail_on_duplicate:
                raise KeyError('UUID %s is already taken by another object %s, cannot add object %s' % (obj.uuid, self._objects[obj.uuid], obj))
            else:
                logger.warning('A duplicate UUID was passed to an ObjectPool for a %s object.' % obj)
                obj.uuid = get_new_uuid()

    def change_all_uuids(self):
        items = list(self._objects.items())
        for uuid, obj in items:
            obj.uuid = get_new_uuid()

    def remove_object(self, obj):
        if obj.uuid in self._objects:
            if self._objects[obj.uuid] == obj:
                del self._objects[obj.uuid]

    def get_object(self, uuid):
        obj = self._objects.get(uuid, None)
        return obj

    def clear(self):
        self._objects.clear()


class ThreadedObjectPool(object):

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.pools = {}

    def clean_pools(self):
        for ptkey in list(self.pools.keys()):
            if ptkey == (None, None) or not ptkey[0].is_alive() or not ptkey[1].is_alive():
                del self.pools[ptkey]

    def get_pool(self):
        process = multiprocessing.current_process()
        thread = threading.current_thread()
        pool = self.pools.get((process, thread), ObjectPool())
        self.pools[(process, thread)] = pool
        return pool

    def add_or_get_object(self, *args, **kwargs):
        pool = self.get_pool()
        return (pool.add_or_get_object)(*args, **kwargs)

    def add_object(self, *args, **kwargs):
        pool = self.get_pool()
        return (pool.add_object)(*args, **kwargs)

    def change_all_uuids(self, *args, **kwargs):
        pool = self.get_pool()
        return (pool.change_all_uuids)(*args, **kwargs)

    def remove_object(self, *args, **kwargs):
        pool = self.get_pool()
        return (pool.remove_object)(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        pool = self.get_pool()
        return (pool.get_object)(*args, **kwargs)

    def clear(self, *args, **kwargs):
        pool = self.get_pool()
        return (pool.clear)(*args, **kwargs)