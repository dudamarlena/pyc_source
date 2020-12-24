# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/setup/utils/instruction_from_parts.py
# Compiled at: 2020-02-02 15:10:16
# Size of source mod 2**32: 2860 bytes
from typing import Sequence
from exactly_lib.instructions.multi_phase.utils.instruction_parts import InstructionParts, InstructionPartsParser
from exactly_lib.section_document.element_parsers.section_element_parsers import InstructionParser
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.source_location import FileSystemLocationInfo
from exactly_lib.symbol.symbol_usage import SymbolUsage
from exactly_lib.test_case.os_services import OsServices
from exactly_lib.test_case.phases.common import InstructionEnvironmentForPreSdsStep, InstructionEnvironmentForPostSdsStep
from exactly_lib.test_case.phases.setup import SetupPhaseInstruction, SetupSettingsBuilder
from exactly_lib.test_case.result import sh, svh
from exactly_lib.test_case.validation.sdv_validation import PreOrPostSdsSvhValidationErrorValidator

class SetupPhaseInstructionFromParts(SetupPhaseInstruction):

    def __init__(self, instruction_setup: InstructionParts):
        self.setup = instruction_setup
        self._validator = PreOrPostSdsSvhValidationErrorValidator(instruction_setup.validator)

    def symbol_usages(self) -> Sequence[SymbolUsage]:
        return self.setup.symbol_usages

    def validate_pre_sds(self, environment: InstructionEnvironmentForPreSdsStep) -> svh.SuccessOrValidationErrorOrHardError:
        return self._validator.validate_pre_sds_if_applicable(environment.path_resolving_environment)

    def validate_post_setup(self, environment: InstructionEnvironmentForPostSdsStep) -> svh.SuccessOrValidationErrorOrHardError:
        return svh.new_svh_success()

    def main(self, environment: InstructionEnvironmentForPostSdsStep, os_services: OsServices, settings_builder: SetupSettingsBuilder) -> sh.SuccessOrHardError:
        validation_result = self._validator.validate_post_sds_if_applicable(environment.path_resolving_environment)
        if not validation_result.is_success:
            return sh.new_sh_hard_error(validation_result.failure_message)
        return self.setup.executor.apply_as_non_assertion(environment, environment.phase_logging, os_services)


class Parser(InstructionParser):

    def __init__(self, instruction_parts_parser: InstructionPartsParser):
        self.instruction_parts_parser = instruction_parts_parser

    def parse(self, fs_location_info: FileSystemLocationInfo, source: ParseSource) -> SetupPhaseInstruction:
        instruction_parts = self.instruction_parts_parser.parse(fs_location_info, source)
        return SetupPhaseInstructionFromParts(instruction_parts)