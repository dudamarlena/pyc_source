# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firstblood/patches/abc.py
# Compiled at: 2018-10-28 14:14:34
# Size of source mod 2**32: 421 bytes


def getAllSubclasses(abc, blacklist):
    res = []
    blacklist = dict.fromkeys(blacklist)
    for klass in object.__subclasses__():
        if issubclass(klass, abc) and klass.__module__ not in blacklist:
            res.append(klass)

    return set(res)


if __name__ == '__main__':
    from collections.abc import Iterable
    its = getAllSubclasses(Iterable)
    print(its)
    from IPython import embed
    embed()