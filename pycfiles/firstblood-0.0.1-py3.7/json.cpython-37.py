# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firstblood/patches/json.py
# Compiled at: 2018-10-28 14:10:52
# Size of source mod 2**32: 499 bytes
import json
from .patch import patch, needFlush

@needFlush
def addMethods():
    patch(dict, 'json', property(json.dumps))
    patch(int, 'json', property(json.dumps))
    patch(list, 'json', property(json.dumps))
    patch(set, 'json', property(json.dumps))
    patch(str, 'json', property(json.dumps))


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