# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/program_modes/test_case/contents_structure/test_case_help.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 636 bytes
from typing import Dict, Sequence
from exactly_lib.help.program_modes.common.contents_structure import SectionDocumentation

class TestCaseHelp(tuple):

    def __new__(cls, phase_helps: Sequence[SectionDocumentation]):
        return tuple.__new__(cls, (list(phase_helps),))

    @property
    def phase_helps_in_order_of_execution(self) -> Sequence[SectionDocumentation]:
        return self[0]

    @property
    def phase_name_2_phase_help(self) -> Dict[(str, SectionDocumentation)]:
        return {ph_help.name.plain:ph_help for ph_help in self.phase_helps_in_order_of_execution}