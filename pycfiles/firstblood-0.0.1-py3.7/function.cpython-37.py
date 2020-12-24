# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firstblood/patches/function.py
# Compiled at: 2018-10-28 14:11:51
# Size of source mod 2**32: 603 bytes
import functools as fn
from types import FunctionType, BuiltinFunctionType
from .patch import patch, needFlush

@needFlush
def addMethods():
    patch(FunctionType, 'partial', fn.partialmethod(fn.partial))
    patch(FunctionType, 'bind', fn.partialmethod(fn.partial))
    patch(BuiltinFunctionType, 'partial', fn.partialmethod(fn.partial))
    patch(BuiltinFunctionType, 'bind', fn.partialmethod(fn.partial))


@needFlush
def patchMethods():
    pass


@needFlush
def patchAll():
    addMethods()
    patchMethods()


if __name__ == '__main__':
    from IPython import embed
    patchAll()
    embed()