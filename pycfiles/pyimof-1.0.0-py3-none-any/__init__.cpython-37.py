# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyimmutable/__init__.py
# Compiled at: 2019-11-05 11:32:56
# Size of source mod 2**32: 4118 bytes
import collections.abc, functools, json
from _pyimmutable import ImmutableDict, ImmutableList, isImmutableJson
__all__ = ('ImmutableDict', 'ImmutableList', 'json_dump', 'json_dumps', 'json_load',
           'json_loads', 'make_immutable', 'make_mutable')
collections.abc.Mapping.register(ImmutableDict)
collections.abc.Sequence.register(ImmutableList)

def make_immutable(object):
    """Make a deep copy of nested sequences/mappings using ``list`` and ``dict``.

A nested structure using ``ImmutableDict``/``ImmutableList`` objects is turned
into an equivalent structure using ``dict`` and ``list``, e.g. for passing
to ``json.dump``."""
    if isinstance(object, collections.abc.Mapping):
        return ImmutableDict(((make_immutable(k), make_immutable(v)) for k, v in object.items()))
    if isinstance(object, collections.abc.Sequence):
        if not isinstance(object, str):
            return ImmutableList((make_immutable(i) for i in object))
    return object


def make_mutable(object):
    """Make a deep copy using ``ImmutableList`` and ``ImmutableDict``.

A nested structure using is turned into one using ``ImmutableList`` for every
sequence and ``ImmutableDict`` for every mapping."""
    if isinstance(object, collections.abc.Mapping):
        return {make_mutable(k):make_mutable(v) for k, v in object.items()}
    if isinstance(object, collections.abc.Sequence):
        if not isinstance(object, str):
            return [make_mutable(i) for i in object]
    return object


@functools.wraps((json.load),
  assigned=(set(functools.WRAPPER_ASSIGNMENTS) - {'__doc__'}))
def json_load(*args, **kwargs):
    """Read JSON from ``fp`` and deserialize as immutable data.

This function calls ``json.load`` and then builds a (potentially nested)
structure of ``ImmutableDict``/``ImmutableList`` objects from the returned
object.

All arguments are passed to ``json.load``. This function may be replaced by
an efficient, native implementation in a later version of pyimmutable, which
may not support the same keyword arguments."""
    return make_immutable((json.load)(*args, **kwargs))


@functools.wraps((json.loads),
  assigned=(set(functools.WRAPPER_ASSIGNMENTS) - {'__doc__'}))
def json_loads(*args, **kwargs):
    """Deserialize JSON string as immutable data.

This function calls ``json.loads`` and then builds a (potentially nested)
structure of ``ImmutableDict``/``ImmutableList`` objects from the returned
object.

All arguments are passed to ``json.loads``. This function may be replaced by
an efficient, native implementation in a later version of pyimmutable, which
may not support the same keyword arguments."""
    return make_immutable((json.loads)(*args, **kwargs))


@functools.wraps((json.dump),
  assigned=(set(functools.WRAPPER_ASSIGNMENTS) - {'__doc__'}))
def json_dump(object, *args, **kwargs):
    """Serialize `obj`` as a JSON and write to ``fp``.

This function makes a deep copy of the object, replacing all sequences
(including ``ImmutableList``) with lists and all mappings (including
``ImmutableDict``) with dicts. The result is passed to ``json.dump``.

All arguments are passed to ``json.dump``. This function may be replaced by
an efficient, native implementation in a later version of pyimmutable, which
may not support the same keyword arguments."""
    return (json.dump)(make_mutable(object), *args, **kwargs)


@functools.wraps((json.dumps),
  assigned=(set(functools.WRAPPER_ASSIGNMENTS) - {'__doc__'}))
def json_dumps(object, *args, **kwargs):
    """Serialize ``obj`` to a JSON formatted ``str``.

This function makes a deep copy of the object, replacing all sequences
(including ``ImmutableList``) with lists and all mappings (including
``ImmutableDict``) with dicts. The result is passed to ``json.dumps``.

All arguments are passed to ``json.dumps``. This function may be replaced by
an efficient, native implementation in a later version of pyimmutable, which
may not support the same keyword arguments."""
    return (json.dumps)(make_mutable(object), *args, **kwargs)