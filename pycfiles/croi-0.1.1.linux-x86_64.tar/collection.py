# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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