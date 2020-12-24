# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/common/help/instruction_documentation.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 1475 bytes
from typing import List, Sequence
from exactly_lib.common.help.syntax_contents_structure import InvokationVariant, SyntaxElementDescription
from exactly_lib.definitions.cross_ref.app_cross_ref import SeeAlsoTarget
from exactly_lib.definitions.doc_format import syntax_text
from exactly_lib.util.textformat.structure.core import StringText, ParagraphItem
from exactly_lib.util.textformat.structure.document import Section

class InstructionDocumentation:
    __doc__ = '\n    Reference documentation about an instruction,\n    à la man page.\n    '

    def __init__(self, instruction_name: str):
        self._instruction_name = instruction_name

    def instruction_name(self) -> str:
        return self._instruction_name

    @property
    def instruction_name_text(self) -> StringText:
        return syntax_text(self._instruction_name)

    def single_line_description(self) -> str:
        raise NotImplementedError()

    def main_description_rest(self) -> List[ParagraphItem]:
        return []

    def main_description_rest_sub_sections(self) -> Sequence[Section]:
        return []

    def invokation_variants(self) -> Sequence[InvokationVariant]:
        return []

    def syntax_element_descriptions(self) -> Sequence[SyntaxElementDescription]:
        return []

    def see_also_targets(self) -> List[SeeAlsoTarget]:
        """
        :returns: A new list of see-also-targets, which may contain duplicate elements.
        """
        return []