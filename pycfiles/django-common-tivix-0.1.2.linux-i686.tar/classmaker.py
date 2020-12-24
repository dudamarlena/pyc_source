# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/django_common/lib/python2.7/site-packages/django_common/classmaker.py
# Compiled at: 2012-03-11 19:20:35
import inspect, types, __builtin__

def skip_redundant(iterable, skipset=None):
    """Redundant items are repeated items or items in the original skipset."""
    if skipset is None:
        skipset = set()
    for item in iterable:
        if item not in skipset:
            skipset.add(item)
            yield item

    return


def remove_redundant(metaclasses):
    skipset = set([types.ClassType])
    for meta in metaclasses:
        skipset.update(inspect.getmro(meta)[1:])

    return tuple(skip_redundant(metaclasses, skipset))


memoized_metaclasses_map = {}

def get_noconflict_metaclass(bases, left_metas, right_metas):
    """Not intended to be used outside of this module, unless you know
    what you are doing."""
    metas = left_metas + tuple(map(type, bases)) + right_metas
    needed_metas = remove_redundant(metas)
    if needed_metas in memoized_metaclasses_map:
        return memoized_metaclasses_map[needed_metas]
    if not needed_metas:
        meta = type
    elif len(needed_metas) == 1:
        meta = needed_metas[0]
    elif needed_metas == bases:
        raise TypeError('Incompatible root metatypes', needed_metas)
    else:
        metaname = '_' + ('').join([ m.__name__ for m in needed_metas ])
        meta = classmaker()(metaname, needed_metas, {})
    memoized_metaclasses_map[needed_metas] = meta
    return meta


def classmaker(left_metas=(), right_metas=()):

    def make_class(name, bases, adict):
        metaclass = get_noconflict_metaclass(bases, left_metas, right_metas)
        return metaclass(name, bases, adict)

    return make_class