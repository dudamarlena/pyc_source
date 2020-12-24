# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/collection.py
# Compiled at: 2020-01-31 11:01:51
# Size of source mod 2**32: 1075 bytes
from typing import Sequence, TypeVar, List

class FrozenSetBasedOnEquality(tuple):

    def __new__(cls, elements: Sequence):
        return tuple.__new__(cls, (tuple(_unique(elements)),))

    @property
    def elements(self) -> Sequence:
        return self[0]

    def union(self, other_set_based_on_equality):
        ret_val = list(self.elements)
        for o in other_set_based_on_equality.elements:
            if o not in self.elements:
                ret_val.append(o)

        return FrozenSetBasedOnEquality(ret_val)


def _unique(elements: Sequence) -> list:
    ret_val = []
    for x in elements:
        if x not in ret_val:
            ret_val.append(x)

    return ret_val


def intersperse_list(element_between, l: list) -> list:
    if len(l) <= 1:
        return l
    else:
        return [
         l[0]] + [element_between] + intersperse_list(element_between, l[1:])


T = TypeVar('T')

def concat_list(list_of_lists: Sequence[Sequence[T]]) -> List[T]:
    ret_val = []
    for element_list in list_of_lists:
        ret_val += element_list

    return ret_val