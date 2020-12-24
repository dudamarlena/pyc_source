# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hues/dpda.py
# Compiled at: 2016-10-02 10:43:01
# Size of source mod 2**32: 1434 bytes
"""Deterministic Push Down Automaton helpers.

This module implements helper functions to allow producing deterministic
representation of arbitrarily chained props.
"""
from functools import reduce, partial

def zero_break(stack):
    """Handle Resets in input stack.
  Breaks the input stack if a Reset operator (zero) is encountered.
  """
    reducer = lambda x, y: tuple() if y == 0 else x + (y,)
    return reduce(reducer, stack, tuple())


def annihilate(predicate, stack):
    """Squash and reduce the input stack.
  Removes the elements of input that match predicate and only keeps the last
  match at the end of the stack.
  """
    extra = tuple(filter(lambda x: x not in predicate, stack))
    head = reduce(lambda x, y: y if y in predicate else x, stack, None)
    if head:
        return extra + (head,)
    return extra


def annihilator(predicate):
    """Build a partial annihilator for given predicate."""
    return partial(annihilate, predicate)


def dedup(stack):
    """Remove duplicates from the stack in first-seen order."""
    reducer = lambda x, y: x if y in x else x + (y,)
    return reduce(reducer, stack, tuple())


def apply(funcs, stack):
    """Apply functions to the stack, passing the resulting stack to next state."""
    return reduce(lambda x, y: y(x), funcs, stack)


__all__ = ('zero_break', 'annihilator', 'dedup', 'apply')