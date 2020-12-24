# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gyukutai/__init__.py
# Compiled at: 2017-01-28 09:44:33
# Size of source mod 2**32: 2965 bytes
import typing, types, collections, forbiddenfruit

class _Base(object):

    def __init__(self, seq: typing.Sequence):
        self.seq = seq


class _FindOr(_Base):
    __doc__ = '\n    An or that exports the `.find` method on lists.\n    '

    def __or__(self, other: typing.Callable[([typing.Any], bool)]):
        if not callable(other):
            cbl = lambda x: x == other
        else:
            cbl = other
        for i in self.seq:
            if cbl(i) is True:
                return i


find_prop = property(fget=lambda l: _FindOr(l), doc='Given a piped callable, finds an object in the list.')

class _ApplyOr(_Base):

    def __or__(self, other):
        if not callable(other):
            return NotImplemented
        result = []
        for item in self.seq:
            result.append(other(item))

        return result


apply_prop = property(fget=lambda l: _ApplyOr(l), doc='Given a piped callable, applies it to all items in the list.')

class _AllOr(_Base):

    def __or__(self, other):
        if not callable(other):
            return NotImplemented
        for item in self.seq:
            if other(item) is not True:
                return False

        return True


all_prop = property(fget=lambda l: _AllOr(l), doc='Given a piped callable, ensures all items return True when provided as an argument to the callable.')

class _AnyOr(_Base):

    def __or__(self, other):
        if not callable(other):
            return NotImplemented
        for item in self.seq:
            if other(item) is True:
                return True

        return False


any_prop = property(fget=lambda l: _AnyOr(l), doc='Given a piped callable, ensures that at least one item matches.')

class _FilterOr(_Base):

    def __or__(self, other):
        if not callable(other):
            return NotImplemented
        results = []
        for item in self.seq:
            if other(item) is True:
                results.append(item)

        return results


filter_prop = property(fget=lambda l: _FilterOr(l), doc='Given a piped callable, filters through all items and returns a new sequence.')

def apply():
    """
    Applies the tweaks to the objectss.
    """
    for victim in [list, tuple, collections.Iterable, type({}.keys()), type({}.values())]:
        forbiddenfruit.curse(victim, 'find', find_prop)
        forbiddenfruit.curse(victim, 'apply', apply_prop)
        forbiddenfruit.curse(victim, 'all', all_prop)
        forbiddenfruit.curse(victim, 'any', any_prop)
        forbiddenfruit.curse(victim, 'filter', filter_prop)