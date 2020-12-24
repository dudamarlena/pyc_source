# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/name_and_value.py
# Compiled at: 2020-02-02 12:38:28
# Size of source mod 2**32: 774 bytes
from typing import Generic, TypeVar, Dict, Sequence
T = TypeVar('T')

class NameAndValue(tuple, Generic[T]):
    __doc__ = '\n    A name with an associated value.\n\n    Is a tuple with two elements - so objects can be used wherever pairs can be used.\n    '

    def __new__(cls, name, value: T):
        return tuple.__new__(cls, (name, value))

    @staticmethod
    def as_dict(elements: 'Sequence[NameAndValue[T]]') -> Dict[(str, T)]:
        return to_dict(elements)

    @property
    def name(self):
        return self[0]

    @property
    def value(self) -> T:
        return self[1]


def to_dict(name_and_values: Sequence[NameAndValue[T]]) -> Dict[(str, T)]:
    return {nav.name:nav.value for nav in name_and_values}