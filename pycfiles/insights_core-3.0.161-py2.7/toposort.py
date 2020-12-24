# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/contrib/toposort.py
# Compiled at: 2019-05-16 13:41:33
from functools import reduce as _reduce
__all__ = [
 'toposort', 'toposort_flatten']

def toposort(data):
    """Dependencies are expressed as a dictionary whose keys are items
and whose values are a set of dependent items. Output is a list of
sets in topological order. The first set consists of items with no
dependences, each subsequent set consists of items that depend upon
items in the preceeding sets.
"""
    if len(data) == 0:
        return
    data = data.copy()
    for k, v in data.items():
        v.discard(k)

    extra_items_in_deps = _reduce(set.union, data.values()) - set(data.keys())
    data.update(dict((item, set()) for item in extra_items_in_deps))
    while True:
        ordered = set(item for item, dep in data.items() if len(dep) == 0)
        if not ordered:
            break
        yield ordered
        data = dict((item, dep - ordered) for item, dep in data.items() if item not in ordered)

    if len(data) != 0:
        raise ValueError(('Cyclic dependencies exist among these items: {}').format((', ').join(repr(x) for x in data.items())))


def toposort_flatten(data, sort=True):
    """Returns a single list of dependencies. For any set returned by
toposort(), those items are sorted and appended to the result (just to
make the results deterministic)."""
    result = []
    for d in toposort(data):
        result.extend((sorted if sort else list)(d))

    return result