# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ghetzel/src/github.com/PerformLine/python-performline-client/build/lib.linux-x86_64-2.7/performline/embedded/stdlib/utils/lists.py
# Compiled at: 2018-05-17 16:01:23
"""
Functions for working with lists
"""
from __future__ import absolute_import
from .types import isiterable

def flatten(value):
    if isiterable(value):
        out = []
        for i, v in enumerate(value):
            if isiterable(v):
                out += flatten(v)
            else:
                out.append(v)

        return out
    return value


def chunkwise(iterable, size=2):
    if size < 2:
        for v in iterable:
            yield v

    else:
        ilen = len(iterable)
        for i, _ in enumerate(iterable):
            if not i % size:
                out = [
                 iterable[i]]
                for j in xrange(size - 1):
                    if i + j + 1 < ilen:
                        out.append(iterable[(i + j + 1)])
                    else:
                        out.append(None)

                yield tuple(out)

    return