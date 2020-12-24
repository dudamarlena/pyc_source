# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/phases/cleanup.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 1479 bytes
from enum import Enum
from typing import Sequence
from exactly_lib.symbol.symbol_usage import SymbolUsage
from exactly_lib.test_case import phase_identifier
from exactly_lib.test_case.os_services import OsServices
from exactly_lib.test_case.phases.common import InstructionEnvironmentForPostSdsStep, InstructionEnvironmentForPreSdsStep, TestCaseInstructionWithSymbols
from exactly_lib.test_case.result import svh
from exactly_lib.test_case.result.sh import SuccessOrHardError

class PreviousPhase(Enum):
    SETUP = 1
    ACT = 2
    BEFORE_ASSERT = 3
    ASSERT = 4


class CleanupPhaseInstruction(TestCaseInstructionWithSymbols):
    __doc__ = '\n    Abstract base class for instructions of the CLEANUP phase.\n    '

    @property
    def phase(self) -> phase_identifier.Phase:
        return phase_identifier.CLEANUP

    def validate_pre_sds(self, environment: InstructionEnvironmentForPreSdsStep) -> svh.SuccessOrValidationErrorOrHardError:
        return svh.new_svh_success()

    def main(self, environment: InstructionEnvironmentForPostSdsStep, os_services: OsServices, previous_phase: PreviousPhase) -> SuccessOrHardError:
        """
        :param previous_phase: The phase that was executed directly before the cleanup phase.
        """
        raise NotImplementedError()


def get_symbol_usages(instruction: CleanupPhaseInstruction) -> Sequence[SymbolUsage]:
    return instruction.symbol_usages()