# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firstblood/patches/float.py
# Compiled at: 2018-10-28 14:12:01
# Size of source mod 2**32: 568 bytes
import math
from .patch import patch, needFlush

def tofixed(n, s):
    return f"%.{s}f" % n


@needFlush
def addMethods():
    patch(float, 'int', property(int))
    patch(float, 'str', property(str))
    patch(float, 'fixed', tofixed)
    patch(float, 'ceil', property(math.ceil))
    patch(float, 'floor', property(math.floor))
    patch(float, 'round', property(round))


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