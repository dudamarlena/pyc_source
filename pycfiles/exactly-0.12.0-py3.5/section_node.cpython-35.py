# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/section_target_hierarchy/section_node.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 1572 bytes
from typing import Set, Optional
from exactly_lib.util.textformat.constructor.environment import ConstructionEnvironment
from exactly_lib.util.textformat.constructor.section import SectionItemConstructor
from exactly_lib.util.textformat.section_target_hierarchy.targets import TargetInfoNode
from exactly_lib.util.textformat.structure import document as doc

class SectionItemNodeEnvironment:

    def __init__(self, toc_section_item_tags: Set[str]):
        self._toc_section_item_tags = toc_section_item_tags

    @property
    def toc_section_item_tags(self) -> Set[str]:
        return self._toc_section_item_tags


class SectionItemNode:
    __doc__ = '\n    A node at a fixed position in the tree of sections with corresponding targets.\n\n    Supplies one method for getting the target-hierarchy\n    (for rendering a TOC),\n    and one method for getting the corresponding section-hierarchy\n    (for rendering the contents).\n    '

    def target_info_node(self) -> Optional[TargetInfoNode]:
        """
        :return: Not None iff the section should appear in the TOC
        """
        raise NotImplementedError()

    def section_item_constructor(self, node_environment: SectionItemNodeEnvironment) -> SectionItemConstructor:
        raise NotImplementedError()

    def section_item(self, node_environment: SectionItemNodeEnvironment, construction_environment: ConstructionEnvironment) -> doc.SectionItem:
        """Short cut"""
        return self.section_item_constructor(node_environment).apply(construction_environment)