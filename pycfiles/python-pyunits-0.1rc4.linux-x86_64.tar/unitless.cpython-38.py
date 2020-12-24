# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/unitless.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 5491 bytes
from typing import Union
import numpy as np
from .exceptions import UnitError
from .types import Numeric, UnitValue
from .unit_base import UnitBase
from .unit_interface import UnitInterface
from .unit_type import UnitType

class UnitlessType(UnitType):
    __doc__ = "\n    A UnitType that represents a unitless value. This may seem kind of silly,\n    but it makes things easier in some regards, because it allows us to\n    do things like guarantee that a division operation always returns a unit\n    and not occasionally a raw value, and to represent constructs like\n    s ^ -1.\n\n    We make it so that UnitlessTypes are not compatible with anything. You\n    might think it more logical to instead have them be compatible with\n    everything, but this introduces a nasty reflexivity problem into\n    compatibility checks, e.g. the result is different depending on\n    whether you do a.is_compatible(b) or b.is_compatible(a). Furthermore,\n    I think it's better for PyUnits to force users to initialize a new\n    unit if they want to give a unit-less value units, instead of just\n    doing it implicitly.\n    "


@UnitlessType.decorate
class Unitless(UnitBase):
    __doc__ = '\n    Represents a unit-less value. By design, these are pretty locked-down, so\n    that generally the user has to explicitly extract the raw value in order\n    to do anything with them.\n    '

    def __init__(self, unit_type, value):
        """
        :param unit_type: The UnitlessType instance used to create this class.
        :param value: The unitless value to wrap.
        """
        super().__init__(unit_type)
        if isinstance(value, UnitInterface):
            if not value.type.is_compatible(self.type):
                raise UnitError('To initialize a Unitless value from another unit, you must explicitly take the raw value.')
            self._Unitless__value = value.raw
        else:
            self._Unitless__value = np.asarray(value)

    def __mul__(self, other: UnitValue) -> UnitInterface:
        """
        See superclass for documentation.
        """
        if not isinstance(other, UnitInterface):
            return self.type(self.raw * other)
        if isinstance(other, type(self)):
            return self.type(self.raw * other.raw)
        return NotImplemented

    def __truediv__(self, other: UnitValue) -> UnitInterface:
        """
        See superclass for documentation.
        """
        if not isinstance(other, UnitInterface):
            return self.type(self.raw / other)
        if isinstance(other, type(self)):
            return self.type(self.raw / other.raw)
        return NotImplemented

    def __rtruediv__(self, other: UnitValue) -> UnitInterface:
        assert not isinstance(other, UnitInterface)
        return self.type(other / self.raw)

    def __add__(self, other: UnitValue) -> UnitInterface:
        if not isinstance(other, UnitInterface):
            return self.type(self.raw + other)
        if isinstance(other, type(self)):
            return self.type(self.raw + other.raw)
        return NotImplemented

    @classmethod
    def is_standard(cls) -> bool:
        """
        See superclass for documentation.
        """
        return True

    def to_standard(self) -> 'Unitless':
        """
        See superclass for documentation.
        """
        return self

    @property
    def raw(self) -> np.ndarray:
        """
        See superclass for documentation.
        """
        return self._Unitless__value

    @property
    def name(self) -> str:
        """
        See superclass for documentation.
        """
        return ''

    def cast_to(self, out_type: UnitType) -> UnitInterface:
        """
        See superclass for documentation.
        """
        raise NotImplementedError('A unitless value should not ever need to be casted.')