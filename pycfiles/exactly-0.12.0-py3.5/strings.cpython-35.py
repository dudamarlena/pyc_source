# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/strings.py
# Compiled at: 2019-12-27 10:07:29
# Size of source mod 2**32: 1795 bytes
from abc import ABC
from typing import Any, Mapping, Callable, TypeVar, Generic, Sequence
ToStringObject = Any

class StringConstructor(ABC):
    __doc__ = 'Base classes for some objects that are ToStringObject'

    def __str__(self) -> str:
        pass


class Concatenate(StringConstructor):

    def __init__(self, elements: Sequence[ToStringObject]):
        """
        :param elements: List of elements that supports __str__
        """
        self._elements = elements

    def __str__(self) -> str:
        return ''.join([str(x) for x in self._elements])


class FormatMap(StringConstructor):

    def __init__(self, format_str: str, format_map: Mapping[(str, ToStringObject)]):
        self._format_str = format_str
        self._format_map = format_map

    def __str__(self) -> str:
        return self._format_str.format_map(self._format_map)


class FormatPositional(StringConstructor):

    def __init__(self, format_str: str, *args):
        self._format_str = format_str
        self._args = args

    def __str__(self) -> str:
        return self._format_str.format(*self._args)


T = TypeVar('T')

class Transformed(Generic[T], StringConstructor):

    def __init__(self, x: T, transformer: Callable[([T], str)]):
        self.x = x
        self._transformer = transformer

    def __str__(self) -> str:
        return self._transformer(self.x)


class Function(StringConstructor):

    def __init__(self, function: Callable[([], str)]):
        self._function = function

    def __str__(self) -> str:
        return self._function()


class Repr(StringConstructor):

    def __init__(self, x: ToStringObject):
        self._x = x

    def __str__(self) -> str:
        return repr(str(self._x))