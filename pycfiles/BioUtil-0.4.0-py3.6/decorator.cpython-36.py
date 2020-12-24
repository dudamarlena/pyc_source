# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/BioUtil/decorator.py
# Compiled at: 2016-06-29 03:39:30
# Size of source mod 2**32: 555 bytes
import contextlib, types

def context_decorator(cls):
    """decorator for class, add __enter__ and __exit__ method"""

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        try:
            self.close()
        finally:
            return

    default_attr = {'__enter__':__enter__, 
     '__exit__':__exit__}
    for attr in default_attr.keys():
        if not hasattr(cls, attr):
            setattr(cls, attr, default_attr[attr])

    return cls