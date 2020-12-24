# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/unit.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 4017 bytes
import abc, numpy as np
from .compound_units import Div, Mul
from .exceptions import UnitError
from .arithmetic_helpers import do_mul, do_div, do_add
from .types import CompoundTypeFactories, UnitValue
from .unit_base import UnitBase
from .unit_interface import UnitInterface
from .unit_type import UnitType

class Unit(UnitBase, abc.ABC):
    __doc__ = '\n    Base class for all units.\n    '
    COMPOUND_TYPE_FACTORIES = CompoundTypeFactories(mul=Mul, div=Div)

    def __init__(self, unit_type, value):
        """
        Initializes a new value of this unit.
        :param unit_type: The associated UnitType for this unit.
        :param value: The same value, in some other units, or as a raw numpy
        array.
        """
        super().__init__(unit_type)
        if isinstance(value, UnitInterface):
            if not value.type.is_compatible(self.type):
                raise UnitError('Cannot convert unit of type {} to unit of type {}.'.format(value.type_class, self.type_class))
            standard = value.to_standard()
            self._from_standard(standard)
        else:
            self._set_raw(np.asarray(value))

    def __mul__(self, other: UnitValue) -> UnitInterface:
        return do_mul(self.COMPOUND_TYPE_FACTORIES, self, other)

    def __truediv__(self, other: UnitValue) -> UnitInterface:
        return do_div(self.COMPOUND_TYPE_FACTORIES, self, other)

    def __rtruediv__(self, other: UnitValue) -> UnitInterface:
        return do_div(self.COMPOUND_TYPE_FACTORIES, other, self)

    def __add__(self, other: UnitValue) -> UnitInterface:
        return do_add(self, other)

    def _set_raw(self, raw: np.ndarray) -> None:
        """
        Initializes this class with the given numeric value.
        :param raw: The raw value to use.
        """
        self._Unit__value = raw

    @abc.abstractmethod
    def _from_standard(self, standard_value: 'StandardUnit') -> None:
        """
        Initializes this unit from a different unit with a "standard" value.
        :param standard_value: The standard unit to initialize from.
        """
        pass

    @classmethod
    def is_standard(cls) -> bool:
        """
        See superclass for documentation.
        """
        return False

    @property
    def raw(self) -> np.ndarray:
        """
        See superclass for documentation.
        """
        return self._Unit__value

    @property
    def name(self) -> str:
        """
        See superclass for documentation.
        """
        return self.__class__.__name__

    def cast_to(self, out_type: UnitType) -> UnitInterface:
        """
        See superclass for documentation.
        """
        out_type_class = out_type.__class__
        return out_type(self.type.as_type(self, out_type_class))


class StandardUnit(Unit):
    __doc__ = '\n    Can be inherited from to identify that a particular unit is the "standard"\n    unit for its UnitType. This is useful for two reasons: It makes standard\n    units "explicit", so we can do nice things like raise an exception when we\n    don\'t have one. Also, it saves us from having to write boilerplate code for\n    standard units.\n    '

    def _from_standard(self, standard_value: 'StandardUnit') -> None:
        """
        See superclass for documentation.
        """
        self._set_raw(standard_value.raw)

    @classmethod
    def is_standard(cls) -> bool:
        """
        See superclass for documentation.
        """
        return True

    def to_standard(self) -> Unit:
        """
        See superclass for documentation.
        """
        return self