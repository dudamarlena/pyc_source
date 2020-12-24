# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/description_tree/custom_renderers.py
# Compiled at: 2020-01-31 11:01:50
# Size of source mod 2**32: 1118 bytes
from exactly_lib.definitions import logic
from exactly_lib.type_system.description.tree_structured import StructureRenderer, WithTreeStructureDescription
from exactly_lib.util.description_tree import renderers
from exactly_lib.util.description_tree.renderer import NodeRenderer
from exactly_lib.util.description_tree.tree import Node
from exactly_lib.util.logic_types import ExpectationType

def negation(negated: NodeRenderer[None]) -> NodeRenderer[None]:
    return renderers.NodeRendererFromParts(logic.NOT_OPERATOR_NAME, None, (), (
     negated,))


def positive_or_negative(expectation_type: ExpectationType, original: StructureRenderer) -> StructureRenderer:
    if expectation_type is ExpectationType.POSITIVE:
        return original
    return negation(original)


class WithTreeStructure(NodeRenderer[None]):

    def __init__(self, tree_structured: WithTreeStructureDescription):
        self._tree_structured = tree_structured

    def render(self) -> Node[None]:
        return self._tree_structured.structure().render()