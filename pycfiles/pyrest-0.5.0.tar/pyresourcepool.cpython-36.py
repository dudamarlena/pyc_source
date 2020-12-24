# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyresourcepool/pyresourcepool.py
# Compiled at: 2020-05-12 00:01:20
# Size of source mod 2**32: 4382 bytes
__doc__ = ' Basic python object resource pool.\n'
import copy, time
from threading import RLock
from contextlib import contextmanager

class AllResourcesRemoved(Exception):
    """AllResourcesRemoved"""
    pass


class ObjectAlreadyInPool(Exception):
    """ObjectAlreadyInPool"""
    pass


class ObjectNotInPool(Exception):
    """ObjectNotInPool"""
    pass


class ResourcePool(object):

    def __init__(self, objects):
        """
        Instantiate with a list of objects you want in the resource pool.
        """
        self._objects = objects
        self._removed = {}
        for o in self._objects:
            self._removed[id(o)] = False

        self._available = copy.copy(objects)
        self._lock = RLock()

    def all_removed(self):
        return all(self._removed[id(o)] for o in self._objects)

    def add(self, obj):
        if type(obj) is not list:
            obj = [
             obj]
        with self._lock:
            for o in obj:
                if o in self._objects:
                    raise ObjectAlreadyInPool('Object is already in the pool.')
                self._objects.append(o)
                self._available.append(o)
                self._removed[id(o)] = False

    def remove(self, obj):
        with self._lock:
            if obj not in self._objects:
                raise ObjectNotInPool('Object is not in the list of pool objects.')
            self._removed[id(obj)] = True
            self._available = [o for o in self._available if o is not obj]
            if self.all_removed():
                raise AllResourcesRemoved('All resources have been removed. Further use of the resource pool is void.')

    def get_resource_unmanaged(self, block=True):
        """
        Gets a resource from the pool but in an "unmanaged" fashion. It is
        up to you to return the resource to the pool by calling
        return_resourc().

        Return value is an object from the pool but see the note below.

        NOTE:
        You should consider using get_resource() instead in a 'with' statement
        as this will handle returning the resource automatically. eg:

            with get_resrouce() as r:
                do_stuff(r)

        The resource will be automatically returned upon exiting the 'with'
        block.
        """
        obj = None
        while True:
            with self._lock:
                if self.all_removed():
                    raise AllResourcesRemoved('All resources have been removed. Further use of the resource pool is void.')
                if self._available:
                    obj = self._available.pop(0)
            if obj or not block:
                break
            time.sleep(0.1)

        return obj

    def return_resource(self, obj):
        if obj:
            if obj in self._objects:
                with self._lock:
                    if not self._removed[id(obj)]:
                        self._available.append(obj)

    @contextmanager
    def get_resource(self, block=True):
        """
        Intended to be used in a 'with' statement or a contextlib.ExitStack.

        Returns an object from the pool and waits if necessary. If 'block' is
        False, then None is returned if the pool has been depleted.

        Example useage:

            with get_resrouce() as r:
                do_stuff(r)
            # at this point, outside the with block, the resource has
            # been returned to the pool.
        """
        obj = None
        try:
            obj = self.get_resource_unmanaged(block=block)
            yield obj
        finally:
            self.return_resource(obj)