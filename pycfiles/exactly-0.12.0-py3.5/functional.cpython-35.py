# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/functional.py
# Compiled at: 2020-01-29 09:08:18
# Size of source mod 2**32: 1281 bytes
import types
from typing import TypeVar, Optional, Callable, List, Sequence

def compose_first_and_second(f, g):
    return Composition(g, f)


class Composition:

    def __init__(self, g, f):
        self.g = g
        self.f = f

    def __call__(self, arg):
        return self.g(self.f(arg))


def and_predicate(predicates: list) -> types.FunctionType:
    if not predicates:
        return lambda x: True
    if len(predicates) == 1:
        return predicates[0]
    return _AndPredicate(predicates)


class _AndPredicate:

    def __init__(self, predicates: list):
        self.predicates = predicates

    def __call__(self, *args, **kwargs):
        for predicate in self.predicates:
            if not predicate(*args, **kwargs):
                return False

        return True


T = TypeVar('T')
U = TypeVar('U')

def map_optional(f: Callable[([T], U)], x: Optional[T]) -> Optional[U]:
    if x is None:
        return
    return f(x)


def reduce_optional(f: Callable[([T], U)], value_if_none: U, x: Optional[T]) -> U:
    if x is None:
        return value_if_none
    return f(x)


def filter_not_none(xs: Sequence[Optional[T]]) -> List[T]:
    return [x for x in xs if x is not None]