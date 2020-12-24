# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/section_target_hierarchy/generator.py
# Compiled at: 2018-09-23 12:54:55
# Size of source mod 2**32: 625 bytes
from exactly_lib.util.textformat.section_target_hierarchy.section_node import SectionItemNode
from exactly_lib.util.textformat.section_target_hierarchy.targets import TargetInfoFactory

class SectionHierarchyGenerator:
    __doc__ = '\n    Generates a section with sub sections that may appear in a TOC.\n\n    Can be put anywhere in a section hierarchy - it does not have\n    a fixed position.\n    '

    def generate(self, target_factory: TargetInfoFactory) -> SectionItemNode:
        """
        :param target_factory: Represents the root position of the generated
        section
        """
        raise NotImplementedError()