# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/concurrent/locked_structure.py
# Compiled at: 2020-04-25 10:46:39
# Size of source mod 2**32: 1314 bytes
import threading, typing as tp
from ..structures.proxy import Proxy
T = tp.TypeVar('T')

class LockedStructure(Proxy, tp.Generic[T]):
    __doc__ = '\n    A wizard to make every Python structure thread-safe.\n\n    It wraps obj_to_wrap, passing on all calls, settings and so on to the object wrapper,\n    from lock exposing only the context manager protocol.\n\n    Example:\n\n    >>> locked_dict = LockedStructure(dict)\n    >>> with locked_dict:\n    >>>     locked_dict[5] = 2\n    \n    Also, please note that operations such as addition will strip this object of being a locked\n    structure, ie. they will return object that participated in locked structure plus some other.\n    \n    Note that in-place operations return the locked structure.\n    '
    __slots__ = ('__lock', )

    def __init__(self, obj_to_wrap, lock=None):
        super().__init__(obj_to_wrap)
        self._LockedStructure__lock = lock or threading.Lock()

    def __setattr__(self, key, value):
        if key == '_LockedStructure__lock':
            object.__setattr__(self, key, value)
        else:
            super().__setattr__(key, value)

    def __enter__(self):
        self._LockedStructure__lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._LockedStructure__lock.release()
        return False