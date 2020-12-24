# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/phases/assert_.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 1728 bytes
from enum import Enum
from typing import Sequence
from exactly_lib.symbol.symbol_usage import SymbolUsage
from exactly_lib.test_case import phase_identifier
from exactly_lib.test_case.os_services import OsServices
from exactly_lib.test_case.phases.common import InstructionEnvironmentForPostSdsStep, InstructionEnvironmentForPreSdsStep, TestCaseInstructionWithSymbols
from exactly_lib.test_case.result import pfh, svh

class AssertPhaseInstruction(TestCaseInstructionWithSymbols):
    __doc__ = '\n    Abstract base class for instructions of the ASSERT phase.\n    '

    @property
    def phase(self) -> phase_identifier.Phase:
        return phase_identifier.ASSERT

    def validate_pre_sds(self, environment: InstructionEnvironmentForPreSdsStep) -> svh.SuccessOrValidationErrorOrHardError:
        return svh.new_svh_success()

    def validate_post_setup(self, environment: InstructionEnvironmentForPostSdsStep) -> svh.SuccessOrValidationErrorOrHardError:
        return svh.new_svh_success()

    def main(self, environment: InstructionEnvironmentForPostSdsStep, os_services: OsServices) -> pfh.PassOrFailOrHardError:
        raise NotImplementedError()


class AssertPhasePurpose(Enum):
    ASSERTION = 1
    BOTH = 2
    HELPER = 3


class WithAssertPhasePurpose:
    __doc__ = 'Interface that makes it possible to group assert phase instructions.'

    @property
    def assert_phase_purpose(self) -> AssertPhasePurpose:
        return AssertPhasePurpose.ASSERTION


def get_symbol_usages(instruction: AssertPhaseInstruction) -> Sequence[SymbolUsage]:
    return instruction.symbol_usages()