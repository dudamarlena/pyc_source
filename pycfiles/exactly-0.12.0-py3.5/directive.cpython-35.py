# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/concepts/objects/directive.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1567 bytes
from typing import List
from exactly_lib.definitions.cross_ref.app_cross_ref import SeeAlsoTarget
from exactly_lib.definitions.entity import concepts
from exactly_lib.definitions.entity.directives import ALL_DIRECTIVES
from exactly_lib.help.entities.concepts.contents_structure import ConceptDocumentation
from exactly_lib.util.description import DescriptionWithSubSections
from exactly_lib.util.textformat.structure import structures as docs
from exactly_lib.util.textformat.textformat_parser import TextParser

class _DirectiveConcept(ConceptDocumentation):

    def __init__(self):
        super().__init__(concepts.DIRECTIVE_CONCEPT_INFO)

    def purpose(self) -> DescriptionWithSubSections:
        parse = TextParser({'directive': concepts.DIRECTIVE_CONCEPT_INFO.name, 
         'instruction': concepts.INSTRUCTION_CONCEPT_INFO.name, 
         'symbol': concepts.SYMBOL_CONCEPT_INFO.name})
        contents = parse.fnap(_DESCRIPTION)
        return DescriptionWithSubSections(self.single_line_description(), docs.section_contents(contents))

    def see_also_targets(self) -> List[SeeAlsoTarget]:
        return [d.cross_reference_target for d in ALL_DIRECTIVES]


DIRECTIVE_CONCEPT = _DirectiveConcept()
_DESCRIPTION = '{directive:a/u} is processed during file reading and syntax checking.\n\nNothing happens at later processing steps -\ni.e. unlike {instruction:s}, there is no\nexecution.\n\n\nA consequence of this is that {symbol:s} cannot be used.\n'