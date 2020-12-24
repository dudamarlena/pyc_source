# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/okay/tonka/src/plait.py/src/toposort.py
# Compiled at: 2018-01-07 12:38:39
from functools import reduce

def toposort2(data):
    for k, v in data.items():
        v.discard(k)

    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    data.update({item:set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        yield sorted(ordered)
        data = {item:dep - ordered for item, dep in data.items() if item not in ordered}

    assert not data, 'A cyclic dependency exists amongst %r' % data