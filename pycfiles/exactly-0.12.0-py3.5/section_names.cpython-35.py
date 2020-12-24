# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/definitions/test_suite/section_names.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 1094 bytes
from typing import Dict
from exactly_lib.definitions.formatting import SectionName
from exactly_lib.definitions.test_suite import section_names_plain
CONFIGURATION = SectionName(section_names_plain.SECTION_NAME__CONF)
CASES = SectionName(section_names_plain.SECTION_NAME__CASES)
SUITES = SectionName(section_names_plain.SECTION_NAME__SUITS)
ALL = (
 CONFIGURATION,
 CASES,
 SUITES)

def suite_section_name_dictionary() -> Dict[(str, SectionName)]:
    phase_names = {}
    for section in ALL:
        phase_names[suite_section_name_dict_key_for(section.plain)] = section

    return phase_names


def suite_section_name_dict_key_for(section_name: str) -> str:
    return section_name.replace('-', '_')


CASE__SETUP = SectionName(section_names_plain.SECTION_NAME__CASE_SETUP)
CASE__ACT = SectionName(section_names_plain.SECTION_NAME__CASE_ACT)
CASE__BEFORE_ASSERT = SectionName(section_names_plain.SECTION_NAME__CASE_BEFORE_ASSERT)
CASE__ASSERT = SectionName(section_names_plain.SECTION_NAME__CASE_ASSERT)
CASE__CLEANUP = SectionName(section_names_plain.SECTION_NAME__CASE_CLEANUP)