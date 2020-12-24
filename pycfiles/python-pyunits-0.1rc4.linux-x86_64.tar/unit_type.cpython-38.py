# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/unit_type.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 7638 bytes
from typing import Callable, NamedTuple, Type
import functools
from loguru import logger
from .exceptions import CastError, UnitError
from . import unit_interface
from .interning import Interned
CastFunction = Callable[(['unit_interface.UnitInterface'],
 'unit_interface.UnitInterface')]

class UnitType(Interned):
    __doc__ = '\n    Represents a type of unit.\n\n    Two units are of the same type if we can convert one to the other and back\n    again without losing information. For example, we might have a unit type\n    "Length", and units of this type could be "Meters", "Inches", etc.\n\n    We might be able to convert one unit type to another. This is called\n    casting, and has the potential to lose information.\n    '

    class Cast(NamedTuple):
        __doc__ = '\n        Represents a cast.\n        :param from_type: The type we want to cast from.\n        :param to_type: The type we want to cast to.\n        '
        from_type: Type
        to_type: Type

    _DIRECT_CASTS = {}
    _STANDARD_UNIT_CLASS = None

    def _init_new(self, unit_class: Type) -> None:
        """
        :param unit_class: Allows UnitBaseType classes to be used as class
        decorators for units. This is how we define the type of a unit.
        """
        functools.update_wrapper(self, unit_class)
        self._UnitType__unit_class = unit_class

    def __call__(self, *args, **kwargs) -> 'unit_interface.UnitInterface':
        """
        "Stamps" the unit class so we know what type it is.
        :param args: Will be forwarded to the UnitBase constructor.
        :param kwargs: Will be forwarded to the UnitBase constructor.
        :return: The UnitBase object.
        """
        return (self._UnitType__unit_class)(self, *args, **kwargs)

    @classmethod
    def decorate(cls, unit_class: Type['unit_interface.UnitInterface']) -> 'UnitType':
        """
        Used to decorate a Unit subclass and mark it as a member of this
        UnitType.
        :param unit_class: The Unit subclass that is being decorated.
        :return: The UnitType instance (decorated Unit subclass) that it
        created.
        """
        wrapped = cls.get(unit_class)
        if unit_class.is_standard():
            if cls._STANDARD_UNIT_CLASS is not None:
                raise UnitError('Attempt to set {} as standard unit of {}, which already has standard unit {}.'.format(unit_class.__name__, cls.__name__, cls._STANDARD_UNIT_CLASS.__name__))
            logger.debug('Setting {} as standard unit of type {}.', unit_class.__name__, cls.__name__)
            cls._STANDARD_UNIT_CLASS = wrapped
        return wrapped

    @classmethod
    def register_cast(cls, out_type: Type, handler: CastFunction) -> None:
        """
        Registers a new cast that can be performed.
        :param out_type: The UnitBaseType that we want to be able to convert
        this one too.
        :param handler: The function that will perform this cast.
        """
        cast = cls.Cast(from_type=cls, to_type=out_type)
        logger.debug('Registering cast: {}', cast)
        cls._DIRECT_CASTS[cast] = handler

    @classmethod
    def as_type(cls, unit: 'unit_interface.UnitInterface', out_type: Type) -> 'unit_interface.UnitInterface':
        """
        Casts the wrapped unit to a new type.
        :param unit: The unit instance to convert.
        :param out_type: The unit type to cast to.
        :return: An equivalent unit of the specified type.
        """
        from_type = cls
        logger.debug('Trying to cast from {} to {}.', from_type.__name__, out_type.__name__)
        cast = cls.Cast(from_type=from_type, to_type=out_type)
        if cast not in cls._DIRECT_CASTS:
            raise CastError('Cannot cast from {} to {}.'.format(from_type.__name__, out_type.__name__))
        handler = cls._DIRECT_CASTS[cast]
        return handler(unit)

    def standard_unit_class(self) -> 'UnitType':
        """
        :return: The standard unit class for this UnitType.
        """
        if self._STANDARD_UNIT_CLASS is None:
            raise UnitError('UnitType {} has no standard unit.'.format(self.__class__.__name__))
        return self._STANDARD_UNIT_CLASS

    def is_compatible(self, other: 'UnitType') -> bool:
        """
        Checks if this type is equivalent to another for the purposes of
        conversion.
        :param other: The other type.
        :return: True if the two are equivalent, false otherwise.
        """
        return self.__class__ == other.__class__


class CastHandler:
    __doc__ = "\n    Decorator for handling unit type casts. It can be used as follows:\n\n    @CastHandler(FirstUnit, SecondUnit)\n    def handle_cast(unit: FirstUnit) -> np.ndarray:\n        # Do the conversion and return the value that will be passed to\n        # SecondUnit's ctor.\n    "
    WrappedHandler = Callable[(['unit_interface.UnitInterface'],
     'types.UnitValue')]

    def __init__(self, from_unit: UnitType, to_unit: UnitType):
        """
        :param from_unit: The unit that this handler will take as input.
        :param to_unit: The unit that this handler will produce as output.
        """
        if from_unit.is_compatible(to_unit):
            raise CastError('Units {} and {} are both of type {} and are thus directly convertible.'.format(from_unit.__name__, to_unit.__name__, from_unit.__class__.__name__))
        self._CastHandler__from_unit = from_unit
        self._CastHandler__to_unit = to_unit

    def __call__(self, func: WrappedHandler) -> CastFunction:
        """
        Wraps the function.
        :param func: The function being wrapped.
        :return: The wrapped function.
        """
        functools.update_wrapper(self, func)

        def wrapped(to_convert):
            """
            Wrapper implementation.
            Does the conversion, ensuring that the input and output are in the
            correct units.
            :param to_convert: The UnitBase instance to convert.
            :return: The converted unit instance.
            """
            to_convert = self._CastHandler__from_unit(to_convert)
            raw_output = func(to_convert)
            return self._CastHandler__to_unit(raw_output)

        self._CastHandler__from_unit.register_cast(self._CastHandler__to_unit.__class__, wrapped)
        return wrapped