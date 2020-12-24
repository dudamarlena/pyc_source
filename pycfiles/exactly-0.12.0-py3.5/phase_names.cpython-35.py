# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/definitions/test_case/phase_names.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 940 bytes
from typing import Dict
from exactly_lib.definitions.formatting import SectionName
from exactly_lib.test_case import phase_identifier
CONFIGURATION = SectionName(phase_identifier.CONFIGURATION.identifier)
SETUP = SectionName(phase_identifier.SETUP.section_name)
ACT = SectionName(phase_identifier.ACT.section_name)
BEFORE_ASSERT = SectionName(phase_identifier.BEFORE_ASSERT.section_name)
ASSERT = SectionName(phase_identifier.ASSERT.section_name)
CLEANUP = SectionName(phase_identifier.CLEANUP.section_name)
ALL = (
 CONFIGURATION,
 SETUP,
 ACT,
 BEFORE_ASSERT,
 ASSERT,
 CLEANUP)

def _phase_name_dictionary() -> Dict[(str, SectionName)]:
    phase_names = {}
    for phase in ALL:
        phase_names[phase_name_dict_key_for(phase.plain)] = phase

    return phase_names


def phase_name_dict_key_for(phase_name: str) -> str:
    return phase_name.replace('-', '_')


PHASE_NAME_DICTIONARY = _phase_name_dictionary()