# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firstblood/patches/object.py
# Compiled at: 2018-10-28 14:07:36
# Size of source mod 2**32: 817 bytes
import functools as fn
from .patch import patch, needFlush

class wrap:

    def __init__(self, func, prop=False):
        self.func = func
        self.prop = prop

    def __get__(self, this, cls):
        if this is None:
            this = cls
        if self.prop:
            return self.func(this)
        return fn.partial(self.func, this)


@needFlush
def addMethods():
    patch(object, 'dir', wrap(dir, prop=True))
    patch(object, 'repr', wrap(repr, prop=True))
    patch(object, 'hasattr', wrap(hasattr))
    patch(object, 'getattr', wrap(getattr))
    patch(object, 'setattr', wrap(setattr))


@needFlush
def patchMethods():
    pass


@needFlush
def patchAll():
    patchMethods()
    addMethods()


if __name__ == '__main__':
    from IPython import embed
    patchAll()
    embed()