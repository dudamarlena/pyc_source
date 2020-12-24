# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/program_modes/test_case/render/instruction_set.py
# Compiled at: 2018-09-19 16:40:01
# Size of source mod 2**32: 1212 bytes
from exactly_lib.help.program_modes.common.renderers import instruction_set_constructor
from exactly_lib.help.program_modes.test_case.contents.specification.utils import TestCaseHelpConstructorBase
from exactly_lib.util.textformat.constructor.environment import ConstructionEnvironment
from exactly_lib.util.textformat.structure import document as doc
from exactly_lib.util.textformat.structure import structures as docs
from exactly_lib.util.textformat.structure.structures import text

class InstructionSetPerPhaseRenderer(TestCaseHelpConstructorBase):

    def apply(self, environment: ConstructionEnvironment) -> doc.SectionContents:
        sections = []
        for test_case_phase_help in self.test_case_help.phase_helps_in_order_of_execution:
            if test_case_phase_help.has_instructions:
                renderer = instruction_set_constructor(test_case_phase_help.instruction_set, instruction_group_by=test_case_phase_help.instruction_group_by)
                sections.append(docs.Section(text(test_case_phase_help.name.syntax), renderer.apply(environment)))

        return doc.SectionContents([], sections)