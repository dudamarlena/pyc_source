# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/execution/impl/phase_step_executors.py
# Compiled at: 2019-12-27 10:07:31
# Size of source mod 2**32: 8283 bytes
from typing import Optional
from exactly_lib.execution.impl.single_instruction_executor import ControlledInstructionExecutor, PartialInstructionControlledFailureInfo, PartialControlledFailureEnum
from exactly_lib.test_case.os_services import OsServices
from exactly_lib.test_case.phases import common as instr
from exactly_lib.test_case.phases.assert_ import AssertPhaseInstruction
from exactly_lib.test_case.phases.before_assert import BeforeAssertPhaseInstruction
from exactly_lib.test_case.phases.cleanup import CleanupPhaseInstruction, PreviousPhase
from exactly_lib.test_case.phases.configuration import ConfigurationPhaseInstruction, ConfigurationBuilder
from exactly_lib.test_case.phases.setup import SetupPhaseInstruction, SetupSettingsBuilder
from exactly_lib.test_case.result import pfh, sh, svh

def _from_success_or_validation_error_or_hard_error(res: svh.SuccessOrValidationErrorOrHardError) -> PartialInstructionControlledFailureInfo:
    if res.is_success:
        return
    else:
        if res.is_validation_error:
            return PartialInstructionControlledFailureInfo(PartialControlledFailureEnum.VALIDATION_ERROR, res.failure_message)
        return PartialInstructionControlledFailureInfo(PartialControlledFailureEnum.HARD_ERROR, res.failure_message)


def _from_success_or_hard_error(res: sh.SuccessOrHardError) -> PartialInstructionControlledFailureInfo:
    if res.is_success:
        return
    return PartialInstructionControlledFailureInfo(PartialControlledFailureEnum.HARD_ERROR, res.failure_message)


def _from_pass_or_fail_or_hard_error(res: pfh.PassOrFailOrHardError) -> Optional[PartialInstructionControlledFailureInfo]:
    if res.status is pfh.PassOrFailOrHardErrorEnum.PASS:
        return
    else:
        return PartialInstructionControlledFailureInfo(PartialControlledFailureEnum(res.status.value), res.failure_message)


class ConfigurationMainExecutor(ControlledInstructionExecutor):

    def __init__(self, phase_environment: ConfigurationBuilder):
        self._ConfigurationMainExecutor__phase_environment = phase_environment

    def apply(self, instruction: ConfigurationPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_hard_error(instruction.main(self._ConfigurationMainExecutor__phase_environment))


class SetupValidatePreSdsExecutor(ControlledInstructionExecutor):

    def __init__(self, instruction_environment: instr.InstructionEnvironmentForPreSdsStep):
        self._SetupValidatePreSdsExecutor__instruction_environment = instruction_environment

    def apply(self, instruction: SetupPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_validation_error_or_hard_error(instruction.validate_pre_sds(self._SetupValidatePreSdsExecutor__instruction_environment))


class SetupValidatePostSetupExecutor(ControlledInstructionExecutor):

    def __init__(self, instruction_environment: instr.InstructionEnvironmentForPostSdsStep):
        self._SetupValidatePostSetupExecutor__instruction_environment = instruction_environment

    def apply(self, instruction: SetupPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_validation_error_or_hard_error(instruction.validate_post_setup(self._SetupValidatePostSetupExecutor__instruction_environment))


class SetupMainExecutor(ControlledInstructionExecutor):

    def __init__(self, os_services: OsServices, environment: instr.InstructionEnvironmentForPostSdsStep, setup_settings_builder: SetupSettingsBuilder):
        self._SetupMainExecutor__os_services = os_services
        self._SetupMainExecutor__environment = environment
        self._SetupMainExecutor__setup_settings_builder = setup_settings_builder

    def apply(self, instruction: SetupPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_hard_error(instruction.main(self._SetupMainExecutor__environment, self._SetupMainExecutor__os_services, self._SetupMainExecutor__setup_settings_builder))


class BeforeAssertValidatePostSetupExecutor(ControlledInstructionExecutor):

    def __init__(self, instruction_environment: instr.InstructionEnvironmentForPostSdsStep):
        self._BeforeAssertValidatePostSetupExecutor__instruction_environment = instruction_environment

    def apply(self, instruction: BeforeAssertPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_validation_error_or_hard_error(instruction.validate_post_setup(self._BeforeAssertValidatePostSetupExecutor__instruction_environment))


class AssertValidatePostSetupExecutor(ControlledInstructionExecutor):

    def __init__(self, instruction_environment: instr.InstructionEnvironmentForPostSdsStep):
        self._AssertValidatePostSetupExecutor__instruction_environment = instruction_environment

    def apply(self, instruction: AssertPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_validation_error_or_hard_error(instruction.validate_post_setup(self._AssertValidatePostSetupExecutor__instruction_environment))


class AssertMainExecutor(ControlledInstructionExecutor):

    def __init__(self, environment: instr.InstructionEnvironmentForPostSdsStep, os_services: OsServices):
        self._AssertMainExecutor__environment = environment
        self._AssertMainExecutor__os_services = os_services

    def apply(self, instruction: AssertPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_pass_or_fail_or_hard_error(instruction.main(self._AssertMainExecutor__environment, self._AssertMainExecutor__os_services))


class BeforeAssertValidatePreSdsExecutor(ControlledInstructionExecutor):

    def __init__(self, instruction_environment: instr.InstructionEnvironmentForPreSdsStep):
        self._BeforeAssertValidatePreSdsExecutor__instruction_environment = instruction_environment

    def apply(self, instruction: BeforeAssertPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_validation_error_or_hard_error(instruction.validate_pre_sds(self._BeforeAssertValidatePreSdsExecutor__instruction_environment))


class BeforeAssertMainExecutor(ControlledInstructionExecutor):

    def __init__(self, environment: instr.InstructionEnvironmentForPostSdsStep, os_services: OsServices):
        self._BeforeAssertMainExecutor__environment = environment
        self._BeforeAssertMainExecutor__os_services = os_services

    def apply(self, instruction: BeforeAssertPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_hard_error(instruction.main(self._BeforeAssertMainExecutor__environment, self._BeforeAssertMainExecutor__os_services))


class AssertValidatePreSdsExecutor(ControlledInstructionExecutor):

    def __init__(self, instruction_environment: instr.InstructionEnvironmentForPreSdsStep):
        self._AssertValidatePreSdsExecutor__instruction_environment = instruction_environment

    def apply(self, instruction: AssertPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_validation_error_or_hard_error(instruction.validate_pre_sds(self._AssertValidatePreSdsExecutor__instruction_environment))


class CleanupValidatePreSdsExecutor(ControlledInstructionExecutor):

    def __init__(self, instruction_environment: instr.InstructionEnvironmentForPreSdsStep):
        self._CleanupValidatePreSdsExecutor__instruction_environment = instruction_environment

    def apply(self, instruction: CleanupPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_validation_error_or_hard_error(instruction.validate_pre_sds(self._CleanupValidatePreSdsExecutor__instruction_environment))


class CleanupMainExecutor(ControlledInstructionExecutor):

    def __init__(self, environment: instr.InstructionEnvironmentForPostSdsStep, previous_phase: PreviousPhase, os_services: OsServices):
        self._CleanupMainExecutor__environment = environment
        self._CleanupMainExecutor__previous_phase = previous_phase
        self._CleanupMainExecutor__os_services = os_services

    def apply(self, instruction: CleanupPhaseInstruction) -> PartialInstructionControlledFailureInfo:
        return _from_success_or_hard_error(instruction.main(self._CleanupMainExecutor__environment, self._CleanupMainExecutor__os_services, self._CleanupMainExecutor__previous_phase))