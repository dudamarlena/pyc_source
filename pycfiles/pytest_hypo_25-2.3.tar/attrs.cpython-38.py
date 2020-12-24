# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\strategies\_internal\attrs.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 6771 bytes
from functools import reduce
from itertools import chain
import attr
import hypothesis.strategies as st
from hypothesis.errors import ResolutionFailed
from hypothesis.internal.compat import get_type_hints
from hypothesis.strategies._internal.types import is_a_type, type_sorting_key
from hypothesis.utils.conventions import infer

def from_attrs(target, args, kwargs, to_infer):
    """An internal version of builds(), specialised for Attrs classes."""
    fields = attr.fields(target)
    kwargs = {v:k for k, v in kwargs.items() if v is not infer if v is not infer}
    for name in to_infer:
        kwargs[name] = from_attrs_attribute(getattr(fields, name), target)
    else:
        return st.tuples((st.tuples)(*args), st.fixed_dictionaries(kwargs)).map(lambda value: target(*value[0], **value[1]))


def from_attrs_attribute(attrib, target):
    """Infer a strategy from the metadata on an attr.Attribute object."""
    default = st.nothing()
    if isinstance(attrib.default, attr.Factory):
        default = attrib.default.takes_self or st.builds(attrib.default.factory)
    else:
        if attrib.default is not attr.NOTHING:
            default = st.just(attrib.default)
        else:
            null = st.nothing()
            in_collections = []
            validator_types = set()
            if attrib.validator is not None:
                validator = attrib.validator
                if isinstance(validator, attr.validators._OptionalValidator):
                    null = st.none()
                    validator = validator.validator
                elif isinstance(validator, attr.validators._AndValidator):
                    vs = validator._validators
                else:
                    vs = [
                     validator]
                for v in vs:
                    if isinstance(v, attr.validators._InValidator):
                        if isinstance(v.options, str):
                            in_collections.append(list(all_substrings(v.options)))
                        else:
                            in_collections.append(v.options)
                    elif isinstance(v, attr.validators._InstanceOfValidator):
                        validator_types.add(v.type)
                    elif in_collections:
                        sample = st.sampled_from(list(ordered_intersection(in_collections)))
                        strat = default | null | sample

            else:
                pass
            strat = default | null | types_to_strategy(attrib, validator_types)
        if strat.is_empty:
            raise ResolutionFailed('Cannot infer a strategy from the default, validator, type, or converter for attribute=%r of class=%r' % (
             attrib, target))
        return strat


def types_to_strategy(attrib, types):
    """Find all the type metadata for this attribute, reconcile it, and infer a
    strategy from the mess."""
    if len(types) == 1:
        typ, = types
        if isinstance(typ, tuple):
            return (st.one_of)(*map(st.from_type, typ))
    else:
        return st.from_type(typ)
        if types:
            type_tuples = [k if isinstance(k, tuple) else (k,) for k in types]
            allowed = [t for t in set(sum(type_tuples, ())) if all((issubclass(t, tup) for tup in type_tuples))]
            allowed.sort(key=type_sorting_key)
            return st.one_of([st.from_type(t) for t in allowed])
        if is_a_type(getattr(attrib, 'type', None)):
            return st.from_type(attrib.type)
        converter = getattr(attrib, 'converter', None)
        if isinstance(converter, type):
            return st.from_type(converter)
        if callable(converter):
            hints = get_type_hints(converter)
            if 'return' in hints:
                return st.from_type(hints['return'])
    return st.nothing()


def ordered_intersection(in_):
    """Set union of n sequences, ordered for reproducibility across runs."""
    intersection = reduce(set.intersection, in_, set(in_[0]))
    for x in chain.from_iterable(in_):
        if x in intersection:
            (yield x)
            intersection.remove(x)


def all_substrings(s):
    """Generate all substrings of `s`, in order of length then occurrence.
    Includes the empty string (first), and any duplicates that are present.

    >>> list(all_substrings('010'))
    ['', '0', '1', '0', '01', '10', '010']
    """
    (yield s[:0])
    for n, _ in enumerate(s):
        for i in range(len(s) - n):
            (yield s[i:i + n + 1])