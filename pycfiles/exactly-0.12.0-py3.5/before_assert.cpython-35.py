# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/phases/before_assert.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 1364 bytes
from typing import Sequence
from exactly_lib.symbol.symbol_usage import SymbolUsage
from exactly_lib.test_case import phase_identifier
from exactly_lib.test_case.os_services import OsServices
from exactly_lib.test_case.phases.common import InstructionEnvironmentForPostSdsStep, InstructionEnvironmentForPreSdsStep, TestCaseInstructionWithSymbols
from exactly_lib.test_case.result import sh, svh

class BeforeAssertPhaseInstruction(TestCaseInstructionWithSymbols):
    __doc__ = '\n    Abstract base class for instructions of the BEFORE-ASSERT phase.\n    '

    @property
    def phase(self) -> phase_identifier.Phase:
        return phase_identifier.BEFORE_ASSERT

    def validate_pre_sds(self, environment: InstructionEnvironmentForPreSdsStep) -> svh.SuccessOrValidationErrorOrHardError:
        return svh.new_svh_success()

    def validate_post_setup(self, environment: InstructionEnvironmentForPostSdsStep) -> svh.SuccessOrValidationErrorOrHardError:
        return svh.new_svh_success()

    def main(self, environment: InstructionEnvironmentForPostSdsStep, os_services: OsServices) -> sh.SuccessOrHardError:
        raise NotImplementedError()


def get_symbol_usages(instruction: BeforeAssertPhaseInstruction) -> Sequence[SymbolUsage]:
    return instruction.symbol_usages()