# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/simple_textstruct/rendering/elements.py
# Compiled at: 2020-01-23 16:48:01
# Size of source mod 2**32: 1155 bytes
from typing import TypeVar, Sequence
from exactly_lib.util.render.renderer import SequenceRenderer
from exactly_lib.util.simple_textstruct.structure import Element, Indentation
ELEMENT = TypeVar('ELEMENT', bound=Element)

class IncreasedIndentRenderer(SequenceRenderer[ELEMENT]):

    def __init__(self, renderer: SequenceRenderer[ELEMENT]):
        self._renderer = renderer

    def render_sequence(self) -> Sequence[ELEMENT]:
        ret_val = self._renderer.render_sequence()
        for element in ret_val:
            element.set_properties(element.properties.with_increased_indentation_level)

        return ret_val


class CustomIncreasedIndentRenderer(SequenceRenderer[ELEMENT]):

    def __init__(self, renderer: SequenceRenderer[ELEMENT], increase: Indentation):
        self._renderer = renderer
        self._increase = increase

    def render_sequence(self) -> Sequence[ELEMENT]:
        ret_val = self._renderer.render_sequence()
        for element in ret_val:
            element.set_properties(element.properties.with_increased_indentation(self._increase))

        return ret_val