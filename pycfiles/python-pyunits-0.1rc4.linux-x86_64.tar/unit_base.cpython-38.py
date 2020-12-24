# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/unit_base.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 1937 bytes
from typing import Type
import abc, numpy as np
from .types import UnitValue
from .unit_interface import UnitInterface
from .unit_type import UnitType

class UnitBase(UnitInterface, abc.ABC):
    __doc__ = '\n    Base functionality for all Unit-like objects, including compound units.\n    '

    def __init__(self, my_type: UnitType):
        """
        :param my_type: The associated UnitType for this unit.
        """
        self._UnitBase__type = my_type

    def __str__(self) -> str:
        return '{} {}'.format(self.raw, self.name)

    def __neg__(self) -> UnitInterface:
        return self.type(-self.raw)

    def __radd__(self, other: UnitValue) -> UnitInterface:
        return self.__add__(other)

    def __sub__(self, other: UnitValue) -> UnitInterface:
        return self.__add__(-other)

    def __rsub__(self, other: UnitValue) -> UnitInterface:
        negated = -self
        return negated.__add__(other)

    def __rmul__(self, other: UnitValue) -> UnitInterface:
        return self.__mul__(other)

    def equals(self, other: UnitValue) -> bool:
        this_class = self.type
        other_same = this_class(other)
        return np.array_equal(self.raw, other_same.raw)

    @property
    def type(self) -> UnitType:
        """
        :return: The associated UnitType for this unit.
        """
        return self._UnitBase__type

    @property
    def type_class(self) -> Type:
        """
        :return: The class of the associated UnitType for this unit.
        """
        return self._UnitBase__type.__class__