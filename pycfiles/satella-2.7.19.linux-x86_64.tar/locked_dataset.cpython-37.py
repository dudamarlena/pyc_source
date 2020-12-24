# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/satella/coding/concurrent/locked_dataset.py
# Compiled at: 2020-04-29 12:14:00
# Size of source mod 2**32: 2966 bytes
import inspect, threading
from ..decorators import wraps
from ...exceptions import ResourceLocked, ResourceNotLocked

class LockedDataset:
    __doc__ = '\n    A locked dataset. Subclass like\n\n    >>> class MyDataset(LockedDataset):\n    >>>     def __init__(self):\n    >>>         super(MyDataset, self).__init__()\n    >>>         self.mydata: str = "lol wut"\n    >>>    @LockedDataset.locked\n    >>>    def protected(self):\n    >>>         self.mydata = "updated atomically"\n\n    >>> mds = MyDataset()\n    >>> with mds as md:\n    >>>     md.mydata = "modified atomically"\n\n    >>> try:\n    >>>     with mds(blocking=True, timeout=0.5) as md:\n    >>>         md.mydata = "modified atomically"\n    >>> except ResourceLocked:\n    >>>     print(\'Could not update the resource\')\n\n    If no lock is held, this class that derives from such will raise ResourceNotLocked upon\n    element access while a lock is not being held\n    '

    class InternalDataset(object):
        __slots__ = ('lock', 'locked', 'args')

        def __init__(self):
            self.lock = threading.Lock()
            self.locked = False
            self.args = ()

    def __init__(self):
        self._LockedDataset__internal = LockedDataset.InternalDataset()

    @staticmethod
    def locked(blocking=True, timeout=-1):

        def inner(f):

            @wraps(f)
            def in_ner(self, *args, **kwargs):
                with self(blocking=blocking, timeout=timeout):
                    return f(self, *args, **kwargs)

            return in_ner

        return inner

    def __getattribute__(self, name):
        if inspect.ismethod(super(LockedDataset, self).__getattribute__(name)):
            return super(LockedDataset, self).__getattribute__(name)
        if not get_internal(self).locked:
            raise ResourceNotLocked('No lock held on this object for a read operation')
        return super(LockedDataset, self).__getattribute__(name)

    def __setattr__(self, key, value):
        if key == '_LockedDataset__internal':
            return super(LockedDataset, self).__setattr__(key, value)
        if not get_internal(self).locked:
            raise ResourceNotLocked('No lock held on this object for a write operation')
        return super(LockedDataset, self).__setattr__(key, value)

    def __call__(self, blocking=True, timeout=-1):
        get_internal(self).args = (
         blocking, timeout)
        return self

    def __enter__(self):
        args = get_internal(self).args
        if not (get_internal(self).lock.acquire)(*args):
            raise ResourceLocked('Could not acquire the lock on the object')
        get_internal(self).locked = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        get_internal(self).lock.release()
        get_internal(self).locked = False
        return False


def get_internal(self):
    return super(LockedDataset, self).__getattribute__('_LockedDataset__internal')