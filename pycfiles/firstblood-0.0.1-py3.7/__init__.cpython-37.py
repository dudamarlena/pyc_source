# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firstblood/__init__.py
# Compiled at: 2018-10-28 14:15:49
# Size of source mod 2**32: 949 bytes
from . import patches
from patches.patch import needFlush
from .patches.patch import *
from .patches.int import *
from .patches.float import *
from .patches.str import *
from .patches.bytes import *
from .patches.function import *
from .patches.object import *
from .patches.iterable import *
from .patches.conv import *
from .patches.len import *
from .patches.hash import *
from .patches.json import *
patchesName = [
 'int', 'float', 'str', 'bytes', 'function',
 'object',
 'iterable',
 'conv', 'len', 'hash', 'json']

def importPatch(p):
    return getattr(patches, p)


@needFlush
def addMethods():
    for p in patchesName:
        importPatch(p).addMethods()


@needFlush
def patchMethods():
    for p in patchesName:
        importPatch(p).patchMethods()


@needFlush
def patchAll():
    for p in patchesName:
        importPatch(p).patchAll()


if __name__ == '__main__':
    from IPython import embed
    embed()