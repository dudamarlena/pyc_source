# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_suite/test_suite_doc.py
# Compiled at: 2018-09-19 16:40:01
# Size of source mod 2**32: 1917 bytes
from exactly_lib.section_document.model import SectionContents, ElementType
from exactly_lib.test_case.test_case_doc import TestCase
from exactly_lib.test_suite.instruction_set.sections.cases import CasesSectionInstruction
from exactly_lib.test_suite.instruction_set.sections.configuration.instruction_definition import ConfigurationSectionInstruction
from exactly_lib.test_suite.instruction_set.sections.suites import SuitesSectionInstruction

class TestSuiteDocument(tuple):

    def __new__(cls, configuration_section: SectionContents, suites_section: SectionContents, cases_section: SectionContents, case_phases: TestCase):
        _assert_instruction_class(configuration_section, ConfigurationSectionInstruction)
        _assert_instruction_class(suites_section, SuitesSectionInstruction)
        _assert_instruction_class(cases_section, CasesSectionInstruction)
        return tuple.__new__(cls, (configuration_section,
         suites_section,
         cases_section,
         case_phases))

    @property
    def configuration_section(self) -> SectionContents:
        return self[0]

    @property
    def suites_section(self) -> SectionContents:
        return self[1]

    @property
    def cases_section(self) -> SectionContents:
        return self[2]

    @property
    def case_phases(self) -> TestCase:
        return self[3]


def _assert_instruction_class(phase_contents: SectionContents, instruction_class):
    for element in phase_contents.elements:
        if element.element_type is ElementType.INSTRUCTION:
            if not isinstance(element.instruction_info.instruction, instruction_class):
                raise AssertionError