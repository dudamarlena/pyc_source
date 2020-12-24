# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/dcollins/.env/deleteme/lib/python2.7/site-packages/croi/collection.py
# Compiled at: 2015-03-14 18:42:13
import copy

def updated(left, right, join=lambda l, r: r):
    result = copy.copy(left)
    for k, v in right.iteritems():
        try:
            result[k] = join(left[k], v)
        except KeyError:
            result[k] = v

    return result