# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/phase_identifier.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 1501 bytes
from enum import Enum
from exactly_lib.definitions.test_case import phase_names_plain as names

class PhaseEnum(Enum):
    CONFIGURATION = 0
    SETUP = 1
    ACT = 2
    BEFORE_ASSERT = 3
    ASSERT = 4
    CLEANUP = 5


class Phase(tuple):
    __doc__ = '\n    Class for enumeration of phase constants\n    '

    def __new__(cls, the_enum: PhaseEnum, section_name: str, identifier: str):
        return tuple.__new__(cls, (the_enum, section_name, identifier))

    @property
    def the_enum(self) -> PhaseEnum:
        return self[0]

    @property
    def section_name(self) -> str:
        return self[1]

    @property
    def identifier(self) -> str:
        return self[2]


CONFIGURATION = Phase(PhaseEnum.CONFIGURATION, names.CONFIGURATION_PHASE_NAME, names.CONFIGURATION_PHASE_NAME)
SETUP = Phase(PhaseEnum.SETUP, names.SETUP_PHASE_NAME, names.SETUP_PHASE_NAME)
ACT = Phase(PhaseEnum.ACT, names.ACT_PHASE_NAME, names.ACT_PHASE_NAME)
BEFORE_ASSERT = Phase(PhaseEnum.BEFORE_ASSERT, names.BEFORE_ASSERT_PHASE_NAME, names.BEFORE_ASSERT_PHASE_NAME)
ASSERT = Phase(PhaseEnum.ASSERT, names.ASSERT_PHASE_NAME, names.ASSERT_PHASE_NAME)
CLEANUP = Phase(PhaseEnum.CLEANUP, names.CLEANUP_PHASE_NAME, names.CLEANUP_PHASE_NAME)
PHASES_FOR_PARTIAL_EXECUTION = (
 SETUP, ACT, BEFORE_ASSERT, ASSERT, CLEANUP)
ALL = (
 CONFIGURATION,) + PHASES_FOR_PARTIAL_EXECUTION
ALL_WITH_INSTRUCTIONS = (
 CONFIGURATION, SETUP, BEFORE_ASSERT, ASSERT, CLEANUP)
DEFAULT_PHASE = ACT