# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/simple_textstruct/rendering/line_elements.py
# Compiled at: 2019-12-27 10:07:32
# Size of source mod 2**32: 1061 bytes
from typing import Sequence
from exactly_lib.util.render import combinators as rend_comb
from exactly_lib.util.render.renderer import Renderer, SequenceRenderer
from exactly_lib.util.simple_textstruct.rendering import component_renderers as comp_rend
from exactly_lib.util.simple_textstruct.rendering import line_objects
from exactly_lib.util.simple_textstruct.structure import LineElement, LineObject

class SingleLineObject(SequenceRenderer[LineElement]):

    def __init__(self, line_object: Renderer[LineObject]):
        self._line_object = line_object

    def render_sequence(self) -> Sequence[LineElement]:
        return [
         LineElement(self._line_object.render())]


def single_pre_formatted(s: str) -> SequenceRenderer[LineElement]:
    return SingleLineObject(line_objects.PreFormattedString(s))


def plain_sequence(line_renderers: Sequence[Renderer[LineObject]]) -> SequenceRenderer[LineElement]:
    return rend_comb.SequenceR([comp_rend.LineElementR(line_renderer) for line_renderer in line_renderers])