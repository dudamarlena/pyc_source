# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/program_modes/test_suite/contents_structure/test_suite_help.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 906 bytes
from typing import List, Iterable
from exactly_lib.help.program_modes.common.contents_structure import SectionDocumentation

class TestSuiteHelp(tuple):

    def __new__(cls, test_cases_and_sub_suites_sections: Iterable[SectionDocumentation], test_case_phase_sections: Iterable[SectionDocumentation]):
        cs_list = list(test_cases_and_sub_suites_sections)
        p_list = list(test_case_phase_sections)
        return tuple.__new__(cls, (cs_list + p_list,
         cs_list,
         p_list))

    @property
    def section_helps(self) -> List[SectionDocumentation]:
        return self[0]

    @property
    def test_cases_and_sub_suites_sections(self) -> List[SectionDocumentation]:
        return self[1]

    @property
    def test_case_phase_sections(self) -> List[SectionDocumentation]:
        return self[2]