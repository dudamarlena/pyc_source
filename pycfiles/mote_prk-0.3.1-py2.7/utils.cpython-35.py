# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/mote/mote/utils.py
# Compiled at: 2017-04-24 04:30:52
# Size of source mod 2**32: 2360 bytes
from copy import deepcopy

def _deepmerge(source, delta):
    """Recursive helper"""
    if source is None or delta is None:
        return source
    for key, value in delta.items():
        if isinstance(value, dict):
            if key in source and isinstance(source[key], list):
                _deepmerge(source, {key: [value]})
            else:
                node = source.setdefault(key, {})
                _deepmerge(node, value)
        else:
            if key in source and isinstance(value, list):
                el = deepcopy(source[key][0])
                source[key] = []
                for n in value:
                    if n is not None:
                        source[key].append(deepcopy(el))

                for n, v in enumerate(value):
                    if isinstance(v, dict):
                        _deepmerge(source[key][n], v)
                    elif v is not None:
                        source[key][n] = v

            else:
                source[key] = value

    return source


def deepmerge(source, delta):
    """Return a deep merge of two dictionaries"""
    return _deepmerge(deepcopy(source), delta)


def deephash(o):
    if isinstance(o, (set, tuple, list)):
        return tuple([deephash(e) for e in o])
    if not isinstance(o, dict):
        return hash(o)
    new_o = deepcopy(o)
    for k, v in new_o.items():
        new_o[k] = deephash(v)

    return hash(tuple(frozenset(sorted(new_o.items()))))


def get_object_by_dotted_name(name):
    """Return object identified by eg. a.b.c.d"""
    from mote.models import Project, Aspect, Pattern, Element, Variation
    li = name.split('.')
    length = len(li)
    project = Project(li[0])
    if length == 1:
        return project
    aspect = Aspect(li[1], project)
    if length == 2:
        return aspect
    pattern = Pattern(li[2], aspect)
    if length == 3:
        return pattern
    element = Element(li[3], pattern)
    if length == 4:
        return element
    variation = Variation(li[4], element)
    if length == 5:
        return variation