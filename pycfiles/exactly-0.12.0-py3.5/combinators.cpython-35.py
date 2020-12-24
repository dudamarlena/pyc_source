# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/render/combinators.py
# Compiled at: 2019-12-27 10:07:53
# Size of source mod 2**32: 3257 bytes
from typing import Sequence, Generic, TypeVar
from exactly_lib.util.render.renderer import Renderer, SequenceRenderer
from exactly_lib.util.simple_textstruct import structure
from exactly_lib.util.simple_textstruct.structure import Element, Indentation
T = TypeVar('T')

class ConstantR(Generic[T], Renderer[T]):

    def __init__(self, element: T):
        self._element = element

    def render(self) -> T:
        return self._element


class ConstantSequenceR(Generic[T], SequenceRenderer[T]):

    def __init__(self, elements: Sequence[T]):
        self._elements = elements

    def render_sequence(self) -> Sequence[T]:
        return self._elements


class ConcatenationR(Generic[T], SequenceRenderer[T]):

    def __init__(self, elements: Sequence[SequenceRenderer[T]]):
        self._elements = elements

    def render_sequence(self) -> Sequence[T]:
        ret_val = []
        for element in self._elements:
            ret_val += element.render_sequence()

        return ret_val


class PrependR(Generic[T], SequenceRenderer[T]):

    def __init__(self, first: Renderer[T], following: SequenceRenderer[T]):
        self._first = first
        self._following = following

    def render_sequence(self) -> Sequence[T]:
        ret_val = [self._first.render()]
        ret_val += self._following.render_sequence()
        return ret_val


class AppendR(Generic[T], SequenceRenderer[T]):

    def __init__(self, first: SequenceRenderer[T], last: Renderer[T]):
        self._first = first
        self._last = last

    def render_sequence(self) -> Sequence[T]:
        ret_val = list(self._first.render_sequence())
        ret_val.append(self._last.render())
        return ret_val


class SequenceR(Generic[T], SequenceRenderer[T]):
    __doc__ = '\n    Renders a sequence.\n\n    Special name of the class to avoid clash with builtin name.\n    '

    def __init__(self, elements: Sequence[Renderer[T]]):
        self._elements = elements

    def render_sequence(self) -> Sequence[T]:
        return [element.render() for element in self._elements]


class SingletonSequenceR(Generic[T], SequenceRenderer[T]):
    __doc__ = '\n    Renders a sequence.\n\n    Special name of the class to avoid clash with builtin name.\n    '

    def __init__(self, element: Renderer[T]):
        self._element = element

    def render_sequence(self) -> Sequence[T]:
        return [
         self._element.render()]


ELEMENT = TypeVar('ELEMENT', bound=Element)

class Indented(Generic[ELEMENT], SequenceRenderer[ELEMENT]):

    def __init__(self, original: SequenceRenderer[ELEMENT], indent: Indentation=structure.INDENTATION__1):
        self._original = original
        self._indent = indent

    def render_sequence(self) -> Sequence[ELEMENT]:
        original_elements = self._original.render_sequence()
        return [self._indented(element) for element in original_elements]

    def _indented(self, element: ELEMENT) -> ELEMENT:
        element.set_properties(element.properties.with_increased_indentation(self._indent))
        return element