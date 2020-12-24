# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/concepts/objects/action_to_check.py
# Compiled at: 2019-12-27 10:07:51
# Size of source mod 2**32: 2594 bytes
from typing import List
from exactly_lib.cli.definitions import common_cli_options
from exactly_lib.definitions import formatting, misc_texts
from exactly_lib.definitions.cross_ref.app_cross_ref import SeeAlsoTarget
from exactly_lib.definitions.entity import concepts
from exactly_lib.definitions.entity import conf_params
from exactly_lib.definitions.test_case import phase_infos
from exactly_lib.definitions.test_case.instructions.instruction_names import ACTOR_INSTRUCTION_NAME
from exactly_lib.definitions.test_case.phase_names import PHASE_NAME_DICTIONARY
from exactly_lib.help.entities.concepts.contents_structure import ConceptDocumentation
from exactly_lib.util.description import DescriptionWithSubSections
from exactly_lib.util.textformat.structure import structures as docs
from exactly_lib.util.textformat.textformat_parser import TextParser

class _ActionToCheckConcept(ConceptDocumentation):

    def __init__(self):
        super().__init__(concepts.ACTION_TO_CHECK_CONCEPT_INFO)

    def purpose(self) -> DescriptionWithSubSections:
        parser = TextParser({'action_to_check': concepts.ACTION_TO_CHECK_CONCEPT_INFO.name, 
         'actor': concepts.ACTOR_CONCEPT_INFO.name, 
         'ATC': concepts.ACTION_TO_CHECK_CONCEPT_INFO.acronym, 
         'actor_option': formatting.cli_option(common_cli_options.OPTION_FOR_ACTOR), 
         'actor_instruction': formatting.InstructionName(ACTOR_INSTRUCTION_NAME), 
         'act': phase_infos.ACT.name, 
         'phase': PHASE_NAME_DICTIONARY, 
         'os_process': misc_texts.OS_PROCESS_NAME, 
         'shell_command': formatting.misc_name_with_formatting(misc_texts.SHELL_COMMAND)})
        return DescriptionWithSubSections(concepts.ACTION_TO_CHECK_CONCEPT_INFO.single_line_description, docs.section_contents(parser.fnap(_DESCRIPTION)))

    def see_also_targets(self) -> List[SeeAlsoTarget]:
        return [
         phase_infos.ACT.cross_reference_target,
         concepts.ACTOR_CONCEPT_INFO.cross_reference_target,
         conf_params.ACTOR_CONF_PARAM_INFO.cross_reference_target]


ACTOR_CONCEPT = _ActionToCheckConcept()
_DESCRIPTION = 'The {action_to_check:/q} ({ATC}) is specified jointly by\nthe configured {actor:/q}\nand the contents of the {act} phase.\n\n\nIt is executed as {os_process:a}.\n\n\nDepending on which {actor:/q} is configured,\nthe {ATC} may be, for example:\n\n\n * executable program (with arguments)\n * source code file\n * source code\n * {shell_command}\n'