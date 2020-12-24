# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/simple_textstruct/rendering/components.py
# Compiled at: 2019-12-27 10:07:32
# Size of source mod 2**32: 840 bytes
from abc import ABC
from typing import TypeVar
from exactly_lib.util.render.renderer import Renderer, SequenceRenderer
from exactly_lib.util.simple_textstruct.structure import MajorBlock, MinorBlock, LineElement, LineObject, Document
ELEMENT = TypeVar('ELEMENT')

class DocumentRenderer(Renderer[Document], ABC):

    def render(self) -> Document:
        pass


class MajorBlockRenderer(Renderer[MajorBlock], ABC):
    pass


class MajorBlocksRenderer(SequenceRenderer[MajorBlock], ABC):
    pass


class MinorBlockRenderer(Renderer[MinorBlock], ABC):
    pass


class MinorBlocksRenderer(SequenceRenderer[MinorBlock], ABC):
    pass


class LineElementRenderer(Renderer[LineElement], ABC):
    pass


class LineObjectRenderer(Renderer[LineObject], ABC):
    pass


class LineObjectsRenderer(SequenceRenderer[LineObject], ABC):
    pass