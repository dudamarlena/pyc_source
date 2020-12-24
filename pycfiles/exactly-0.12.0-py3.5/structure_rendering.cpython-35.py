# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/description_tree/structure_rendering.py
# Compiled at: 2020-01-23 16:48:01
# Size of source mod 2**32: 996 bytes
from exactly_lib.util import ansi_terminal_color
from exactly_lib.util.description_tree import simple_textstruct_rendering as rendering
from exactly_lib.util.description_tree.tree import Node
from exactly_lib.util.render.renderer import Renderer, SequenceRenderer
from exactly_lib.util.simple_textstruct import structure as text_struct, structure
from exactly_lib.util.simple_textstruct.structure import MajorBlock, MinorBlock
STRUCTURE_NODE_TEXT_COLOR = ansi_terminal_color.ForegroundColor.CYAN
TREE_LAYOUT = rendering.RenderingConfiguration(Node.header.fget, lambda node_data: rendering.ElementProperties(text_style=text_struct.TextStyle(color=STRUCTURE_NODE_TEXT_COLOR)), structure.INDENTATION__1, '')

def as_major_block(tree: Node[None]) -> Renderer[MajorBlock]:
    return rendering.TreeRenderer(TREE_LAYOUT, tree)


def as_minor_blocks(tree: Node[None]) -> SequenceRenderer[MinorBlock]:
    return rendering.TreeRendererToMinorBlocks(TREE_LAYOUT, tree)