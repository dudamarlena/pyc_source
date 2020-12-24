# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/actors/objects/null_actor.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1535 bytes
from typing import List
from exactly_lib.definitions.entity import actors
from exactly_lib.definitions.entity.concepts import ACTOR_CONCEPT_INFO
from exactly_lib.help.entities.actors.contents_structure import ActorDocumentation
from exactly_lib.util.textformat.structure.core import ParagraphItem
from exactly_lib.util.textformat.structure.document import SectionContents
from exactly_lib.util.textformat.structure.structures import section_contents
from exactly_lib.util.textformat.textformat_parser import TextParser

class NullActorDocumentation(ActorDocumentation):

    def __init__(self):
        super().__init__(actors.NULL_ACTOR)
        format_map = {'null': actors.NULL_ACTOR.singular_name, 
         'actor': ACTOR_CONCEPT_INFO.name.singular}
        self._parser = TextParser(format_map)

    def main_description_rest(self) -> List[ParagraphItem]:
        return self._parser.fnap(_MAIN_DESCRIPTION_REST)

    def act_phase_contents(self) -> SectionContents:
        return section_contents(self._parser.fnap(_ACT_PHASE_CONTENTS))

    def act_phase_contents_syntax(self) -> SectionContents:
        return section_contents(self._parser.fnap(_ACT_PHASE_CONTENTS_SYNTAX))


DOCUMENTATION = NullActorDocumentation()
_ACT_PHASE_CONTENTS = 'Ignored.\n'
_ACT_PHASE_CONTENTS_SYNTAX = 'There are no syntax requirements.\n'
_MAIN_DESCRIPTION_REST = 'The {null} {actor} is useful when the test case does not test a program,\nbut rather properties of the operating system environment.\n'